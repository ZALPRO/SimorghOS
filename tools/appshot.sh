#!/usr/bin/env bash
# SimorghOS — screenshot a specific app from a built ISO.
# usage: sudo tools/appshot.sh <iso> <out.png> <app-query> [boot_seconds] [extra_append]
# Boots, waits for the desktop, opens the rofi launcher (Super+D), types the
# app query, presses Enter, waits, then screendumps via QMP.
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output png}"
QUERY="${3:?app query, e.g. Files}"
WAIT="${4:-900}"
EXTRA="${5:-}"

W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
xorriso -osirrox on -indev "$ISO" \
    -extract /live/vmlinuz "$W/vmlinuz" \
    -extract /live/initrd.img "$W/initrd" >/dev/null 2>&1

QMEM="${QMEM:-1024}"; QCPU="${QCPU:-1}"; QPIN="${QPIN:-1}"
PIN="taskset -c $QPIN"; command -v taskset >/dev/null || PIN=""
$PIN nice -n 19 qemu-system-x86_64 -m "$QMEM" -smp "$QCPU" -cpu max \
    -kernel "$W/vmlinuz" -initrd "$W/initrd" -cdrom "$ISO" \
    -append "boot=live quiet $EXTRA" \
    -device virtio-gpu-pci \
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!
cp "$W/serial.log" "${OUT}.serial" 2>/dev/null || true

echo "waiting ${WAIT}s for the desktop, then opening '$QUERY'…"
sleep "$WAIT"

python3 - "$W/qmp.sock" "$W/shot.ppm" "$QUERY" <<'EOF'
import json, socket, sys, time
sock, out, query = sys.argv[1], sys.argv[2], sys.argv[3]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(sock)
f = s.makefile('rb')
def cmd(o):
    s.sendall((json.dumps(o) + "\n").encode())
    while True:
        r = json.loads(f.readline())
        if "return" in r or "error" in r:
            return r
json.loads(f.readline())
cmd({"execute": "qmp_capabilities"})
def tap(keys, wait=1.5):
    cmd({"execute": "send-key", "arguments": {"keys": keys}})
    time.sleep(wait)
tap([{"key": "meta_l"}, {"key": "d"}], 10)          # rofi drun
for ch in query:
    k = ch.lower()
    if k == " ":
        tap([{"key": "space"}], 0.4)
    elif ch.isdigit():
        tap([{"key": k}], 0.4)
    else:
        tap([{"key": k}], 0.4)
time.sleep(3)
tap([{"key": "ret"}], 12)                            # launch, let it render
cmd({"execute": "screendump", "arguments": {"filename": out}})
print("screendump ok")
EOF

kill $QPID 2>/dev/null || true
cp "$W/serial.log" "${OUT}.serial" 2>/dev/null || true
if command -v convert >/dev/null 2>&1; then
  convert "$W/shot.ppm" "$OUT"
else
  python3 - "$W/shot.ppm" "$OUT" <<'EOF'
import sys, zlib, struct
data = open(sys.argv[1], 'rb').read()
parts = data.split(b'\n', 3)
w, h = map(int, parts[1].split())
raw = parts[3] if len(parts) > 3 else b''
def chunk(t, d):
    c = struct.pack('>I', len(d)) + t + d
    return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
rows = b''.join(b'\x00' + raw[y*w*3:(y+1)*w*3] for y in range(h))
png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
       + chunk(b'IDAT', zlib.compress(rows, 6)) + chunk(b'IEND', b''))
open(sys.argv[2], 'wb').write(png)
EOF
fi
echo "saved: $OUT"
