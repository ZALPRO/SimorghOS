#!/usr/bin/env bash
# SimorghOS — capture real desktop screenshots from a built ISO (QEMU, TCG)
# usage: sudo tools/screenshot.sh <iso> <out.png> [boot_seconds]
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output png}"
WAIT="${3:-240}"

W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
xorriso -osirrox on -indev "$ISO" \
    -extract /live/vmlinuz "$W/vmlinuz" \
    -extract /live/initrd.img "$W/initrd" >/dev/null 2>&1

qemu-system-x86_64 -m 1536 -smp 2 -cpu max \
    -kernel "$W/vmlinuz" -initrd "$W/initrd" -cdrom "$ISO" \
    -append "boot=live quiet" \
    -device virtio-gpu-pci \
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!

echo "waiting ${WAIT}s for the desktop…"
sleep "$WAIT"

python3 - "$W/qmp.sock" "$W/shot.ppm" <<'EOF'
import json, socket, sys, time
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(sys.argv[1])
f = s.makefile('rb')
def cmd(o):
    s.sendall((json.dumps(o) + "\n").encode())
    while True:
        r = json.loads(f.readline())
        if "return" in r or "error" in r:
            return r
json.loads(f.readline())           # greeting
cmd({"execute": "qmp_capabilities"})
cmd({"execute": "screendump", "arguments": {"filename": sys.argv[2]}})
print("screendump ok")
EOF

kill $QPID 2>/dev/null || true
convert "$W/shot.ppm" "$OUT"
echo "saved: $OUT"
