#!/usr/bin/env bash
# SimorghOS — probe via the already-logged-in VGA tty (live-boot autologin).
# usage: sudo tools/serial-probe2.sh <iso> <out-prefix> <shell-command> [wait_s]
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output prefix}"
CMD="${3:-systemctl status simorgh-live-session}"
WAIT="${4:-700}"

W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
xorriso -osirrox on -indev "$ISO" \
    -extract /live/vmlinuz "$W/vmlinuz" \
    -extract /live/initrd.img "$W/initrd" >/dev/null 2>&1

QMEM="${QMEM:-900}"; QCPU="${QCPU:-1}"; QPIN="${QPIN:-1}"
PIN="taskset -c $QPIN"; command -v taskset >/dev/null || PIN=""
$PIN nice -n 19 qemu-system-x86_64 -m "$QMEM" -smp "$QCPU" -cpu max \
    -kernel "$W/vmlinuz" -initrd "$W/initrd" -cdrom "$ISO" \
    -append "boot=live quiet" \
    -device virtio-gpu-pci \
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!

echo "waiting ${WAIT}s for the shell…"
sleep "$WAIT"

python3 - "$W/qmp.sock" "$CMD" "$W/probe.ppm" <<'EOF'
import json, socket, sys, time
sock, cmd, shot = sys.argv[1], sys.argv[2], sys.argv[3]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(sock)
f = s.makefile('rb')
def qmp(o):
    s.sendall((json.dumps(o) + "\n").encode())
    while True:
        r = json.loads(f.readline())
        if "return" in r or "error" in r:
            return r
json.loads(f.readline())
qmp({"execute": "qmp_capabilities"})
def tap(key, wait=0.4):
    qmp({"execute": "send-key", "arguments": {"keys": [key]}})
    time.sleep(wait)
def type_str(txt, wait=0.35):
    for ch in txt:
        if ch == "\n":
            tap("ret", 1.5)
        else:
            tap(ch, wait)
    time.sleep(1)
type_str("clear\n")
time.sleep(2)
type_str("echo PROBE_START\n")
type_str("sudo -i\n")
time.sleep(5)
type_str("user\n")
time.sleep(5)
type_str(cmd + "\n")
time.sleep(15)
type_str("echo PROBE_DONE_MARKER\n")
time.sleep(3)
cmd({"execute": "screendump", "arguments": {"filename": shot}})
EOF

kill $QPID 2>/dev/null || true
if command -v convert >/dev/null 2>&1; then
  convert "$W/probe.ppm" "$OUT.png"
else
  cp "$W/probe.ppm" "$OUT.ppm"
fi
cp "$W/serial.log" "${OUT}.serial" 2>/dev/null || true
echo "probe saved: $OUT.png"
