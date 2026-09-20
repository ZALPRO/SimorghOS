#!/usr/bin/env bash
# SimorghOS — interactive serial probe: boots the ISO, logs in as user,
# runs a shell command, captures the output in the serial log.
# usage: sudo tools/serial-probe.sh <iso> <out-prefix> <shell-command> [wait_s]
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output prefix}"
CMD="${3:-journalctl -u lightdm --no-pager | tail -60}"
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
    -append "boot=live quiet console=ttyS0" \
    -device virtio-gpu-pci \
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial file:"$W/serial.log" &
QPID=$!

echo "waiting ${WAIT}s for the login prompt…"
sleep "$WAIT"

python3 - "$W/qmp.sock" "$CMD" <<'EOF'
import json, socket, sys, time
sock, cmd = sys.argv[1], sys.argv[2]
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
def tap(key, wait=0.35):
    qmp({"execute": "send-key", "arguments": {"keys": [key]}})
    time.sleep(wait)
def type_str(txt, wait=0.3):
    for ch in txt:
        if ch == "\n":
            tap("ret", 1.2)
        elif ch.isalnum() and len(ch) == 1:
            tap(ch, wait)
        elif ch == " ":
            tap("space", wait)
        else:
            tap(ch, wait)
    time.sleep(1)
# login
type_str("user\n")
time.sleep(4)
type_str("user\n")
time.sleep(12)
type_str("sudo -i\n")
time.sleep(4)
type_str("user\n")
time.sleep(4)
type_str(cmd + "\n")
time.sleep(20)
type_str("echo PROBE_DONE_MARKER\n")
time.sleep(2)
EOF

kill $QPID 2>/dev/null || true
cp "$W/serial.log" "${OUT}.serial" 2>/dev/null || true
echo "serial saved: ${OUT}.serial"
