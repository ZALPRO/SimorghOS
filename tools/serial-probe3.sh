#!/usr/bin/env bash
# SimorghOS — diagnostics via a fresh tty (ctrl+alt+F6 login), works even if
# the session grabbed the main display.
# usage: sudo tools/serial-probe3.sh <iso> <out-prefix> <shell-command> [wait_s]
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output prefix}"
CMD="${3:-systemctl is-active simorgh-live-session}"
WAIT="${4:-750}"

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

echo "waiting ${WAIT}s for boot…"
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
def chord(keys, wait=4):
    qmp({"execute": "send-key", "arguments": {"keys": keys}})
    time.sleep(wait)
def tap(key, wait=0.3):
    qmp({"execute": "send-key", "arguments": {"keys": [key]}})
    time.sleep(wait)
def type_str(txt, wait=0.3, ret_wait=2):
    for ch in txt:
        if ch == "\n":
            tap("ret", ret_wait)
        else:
            tap(ch, wait)
    time.sleep(1)
# switch to tty6
chord(["ctrl_l", "alt_l", "f6"], 8)
type_str("user\n", 0.3, 2.5)
time.sleep(3)
type_str("user\n", 0.3, 3)
time.sleep(3)
type_str("clear\n", 0.3, 2)
type_str(cmd + "\n", 0.3, 8)
time.sleep(6)
qmp({"execute": "screendump", "arguments": {"filename": shot}})
print("probe done", flush=True)
EOF

kill $QPID 2>/dev/null || true
if command -v convert >/dev/null 2>&1; then
  convert "$W/probe.ppm" "$OUT.png"
else
  cp "$W/probe.ppm" "$OUT.ppm"
fi
echo "probe saved: $OUT.png"
