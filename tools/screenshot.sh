#!/usr/bin/env bash
# SimorghOS — capture REAL screenshots from a built ISO (QEMU TCG + QMP).
# usage: sudo tools/screenshot.sh <iso> <out.png> [boot_seconds] [extra_append] [keys...]
# keys are QMP send-key names, e.g. meta_l d  (sent as a combo before capture)
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output png}"
WAIT="${3:-240}"
EXTRA="${4:-}"
shift 4 || true
KEYS=("$@")

W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
xorriso -osirrox on -indev "$ISO" \
    -extract /live/vmlinuz "$W/vmlinuz" \
    -extract /live/initrd.img "$W/initrd" >/dev/null 2>&1

qemu-system-x86_64 -m "${RAM:-1200}" -smp 2 -cpu max \
    -kernel "$W/vmlinuz" -initrd "$W/initrd" -cdrom "$ISO" \
    -append "boot=live quiet $EXTRA" \
    -device virtio-gpu-pci \
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!

echo "waiting ${WAIT}s for the desktop…"
sleep "$WAIT"

python3 - "$W/qmp.sock" "$W/shot.ppm" "${KEYS[*]:-}" <<'EOF'
import json, socket, sys, time
sock, out, keys = sys.argv[1], sys.argv[2], sys.argv[3].split()
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
if keys and keys != ['']:
    combo = [{"key": k} for k in keys]
    cmd({"execute": "send-key", "arguments": {"keys": combo}})
    time.sleep(4)
cmd({"execute": "screendump", "arguments": {"filename": out}})
print("screendump ok")
EOF

kill $QPID 2>/dev/null || true
if command -v convert >/dev/null 2>&1; then
  convert "$W/shot.ppm" "$OUT"
else
  python3 - "$W/shot.ppm" "$OUT" <<'EOF'
import sys
def ppm2png(src, dst):
    data = open(src, 'rb').read()
    # parse P6
    parts = data.split(b'\n', 3)
    assert parts[0].strip() == b'P6'
    w, h = map(int, parts[1].split())
    raw = parts[3] if len(parts) > 3 else b''
    import zlib, struct
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    rows = b''.join(b'\x00' + raw[y*w*3:(y+1)*w*3] for y in range(h))
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(rows, 6)) + chunk(b'IEND', b'')
    open(dst, 'wb').write(png)
ppm2png(sys.argv[1], sys.argv[2])
EOF
fi
echo "saved: $OUT"
