#!/usr/bin/env bash
# SimorghOS — diagnostics over a bidirectional serial console (QEMU unix socket).
# Boots with console=ttyS0, waits for the login prompt, types the command,
# saves the full serial transcript + a final screendump.
# usage: sudo tools/serial-probe7.sh <iso> <out-prefix> <shell-command> [wait_s]
set -euo pipefail
ISO="${1:?iso path}"
OUT="${2:?output prefix}"
CMD="${3:-echo KEYTEST}"
WAIT="${4:-1500}"

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
    -vga none \
    -device virtio-gpu-pci \\
    -display none \
    -qmp unix:"$W/qmp.sock",server,nowait \
    -serial unix:"$W/serial.sock",server,nowait \
    -chardev socket,id=ser1,path="$W/ser1.sock",server=on,wait=off \
    -device isa-serial,chardev=ser1 &
QPID=$!

echo "booting with bidirectional serial…"

python3 - "$W/qmp.sock" "$W/ser1.sock" "$CMD" "$W/probe.ppm" "$WAIT" "$W/transcript.txt" <<'EOF'
import json, os, socket, sys, threading, time
qmpsock, serpath, cmd, shot, waitmax = sys.argv[1:6]
waitmax = int(waitmax)
buf = bytearray()
got_login = threading.Event()
got_shell = threading.Event()

def reader():
    while True:
        try:
            c = rs.recv(4096)
        except Exception:
            return
        if not c:
            return
        buf.extend(c)
        tail = bytes(buf[-4000:])
        if b"user@simorgh:" in tail:
            got_shell.set()
            got_login.set()

rs = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
for _ in range(120):
    try:
        rs.connect(serpath)
        break
    except Exception:
        time.sleep(0.5)
else:
    raise SystemExit("serial socket never appeared")
threading.Thread(target=reader, daemon=True).start()

def send(s):
    rs.sendall(s.encode())
    time.sleep(1)

t0 = time.time()
print("waiting for the serial shell (max %ss)…" % waitmax, flush=True)
while not got_login.wait(15):
    if time.time() - t0 > waitmax:
        print("NO LOGIN PROMPT — dumping transcript only", flush=True)
        break
t = time.time() - t0
print("autologin shell ready at %.0fs" % t, flush=True)
send("clear\n")
time.sleep(4)
# wait for D-Bus (early console starts before dbus in the basic phase),
# then run the diagnostic command (bounded: max 120s)
send("for i in $(seq 1 40); do systemctl list-units >/dev/null 2>&1 && break; sleep 3; done\n")
time.sleep(130)
send(cmd + "\n")
time.sleep(30)
send("echo PROBE7_END\n")
time.sleep(8)

qs = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
qs.connect(qmpsock)
qf = qs.makefile('rb')
def qmp(o):
    qs.sendall((json.dumps(o) + "\n").encode())
    while True:
        r = json.loads(qf.readline())
        if "return" in r or "error" in r:
            return r
json.loads(qf.readline())
qmp({"execute": "qmp_capabilities"})
qmp({"execute": "screendump", "arguments": {"filename": shot}})
with open(sys.argv[6], "wb") as fh:
    fh.write(bytes(buf))
print("transcript %d bytes" % len(buf), flush=True)
EOF

kill $QPID 2>/dev/null || true
cp "$W/transcript.txt" "${OUT}.serial" 2>/dev/null || true
if command -v convert >/dev/null 2>&1; then
  convert "$W/probe.ppm" "$OUT.png"
else
  cp "$W/probe.ppm" "$OUT.ppm"
fi
echo "probe saved: $OUT.png / $OUT.serial"
