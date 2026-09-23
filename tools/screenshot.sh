#!/usr/bin/env bash
# SimorghOS — capture REAL screenshots from a built ISO (QEMU TCG + QMP).
# usage: sudo tools/screenshot.sh <iso> <out.png> [boot_seconds] [extra_append] [keys...]
# After boot_seconds it takes up to 6 screendumps at 150s intervals (lavapipe
# first paint under TCG is slow) and keeps the last one.
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output png}"
WAIT="${3:-240}"
EXTRA="${4:-}"
shift 4 || true
KEYS="$*"

W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
xorriso -osirrox on -indev "$ISO" \
    -extract /live/vmlinuz "$W/vmlinuz" \
    -extract /live/initrd.img "$W/initrd" >/dev/null 2>&1

# light by default; override QMEM/QCPU/QPIN for beefier hosts
QMEM="${QMEM:-1024}"; QCPU="${QCPU:-1}"; QPIN="${QPIN:-1}"
PIN="taskset -c $QPIN"; command -v taskset >/dev/null || PIN=""
$PIN nice -n 19 qemu-system-x86_64 -m "$QMEM" -smp "$QCPU" -cpu max \
    -kernel "$W/vmlinuz" -initrd "$W/initrd" -cdrom "$ISO" \
    -append "boot=live quiet $EXTRA" \
    -vga none \
    -device virtio-gpu-pci \\
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!

echo "waiting ${WAIT}s for the desktop…"
sleep "$WAIT"

DUMPS="${DUMPS:-6}"
python3 - "$W/qmp.sock" "$W/shot.ppm" "$KEYS" "$DUMPS" <<'EOF'
import json, socket, sys, time
sock, out, keystr, dumps = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
keys = keystr.split()
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
if keys:
    cmd({"execute": "send-key", "arguments": {"keys": [{"key": k} for k in keys]}})
    time.sleep(6)
# dumps, 150s apart; last one wins
for i in range(dumps):
    if i:
        time.sleep(150)
    cmd({"execute": "screendump", "arguments": {"filename": out}})
    print(f"screendump {i + 1}/{dumps} ok", flush=True)
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
