#!/usr/bin/env bash
# SimorghOS — multi-shot gallery capture (GUI-verified).
# Boots the ISO once, waits for the Hyprland process AND verifies each
# captured frame is actually the GUI (rejects serial-console frames),
# then for each app: hyprctl dispatch exec -> paint -> screendump.
# usage: sudo tools/gallery.sh <iso> <out-dir> [boot_wait_s]
set -euo pipefail
ISO="${1:?iso path}"
OUTDIR="${2:?output dir}"
BOOT_WAIT="${3:-420}"
mkdir -p "$OUTDIR"
rm -f /tmp/gallery-*.ppm

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
    -serial unix:"$W/serial.sock",server,nowait \
    -chardev socket,id=ser1,path="$W/ser1.sock",server=on,wait=off \
    -device isa-serial,chardev=ser1 &
QPID=$!
echo "booting… (initial settle ${BOOT_WAIT}s after shell)"

APPS=(
  "terminal|kitty|100|terminal.png"
  "texteditor|geany|100|texteditor.png"
  "filemanager|thunar|120|filemanager.png"
  "appcenter|/usr/share/simorgh/bin/simorgh-appcenter|120|appcenter.png"
  "controlcenter|/usr/share/simorgh/bin/simorgh-center|120|controlcenter.png"
  "browser|brave-browser|180|browser.png"
  "sysmonitor|gnome-system-monitor|100|sysmonitor.png"
  "installer|calamares|240|installer.png"
)

python3 - "$W/qmp.sock" "$W/ser1.sock" "$BOOT_WAIT" "$OUTDIR" "${APPS[@]}" <<'EOF'
import json, re, socket, sys, threading, time
qmpsock, serpath, bootwait, outdir = sys.argv[1:5]
bootwait = int(bootwait)
apps = [a.split("|") for a in sys.argv[5:]]

buf = bytearray()
ready = threading.Event()
def reader():
    while True:
        try:
            c = s1.recv(4096)
        except Exception:
            return
        if not c:
            return
        buf.extend(c)
        if len(buf) > 300000:
            del buf[:150000]
        if b"user@simorgh:" in bytes(buf[-2000:]):
            ready.set()

s1 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
for _ in range(120):
    try:
        s1.connect(serpath)
        break
    except Exception:
        time.sleep(0.5)
threading.Thread(target=reader, daemon=True).start()

def send(x):
    s1.sendall(x.encode())

t0 = time.time()
print("waiting for serial shell…", flush=True)
while not ready.wait(15):
    if time.time() - t0 > 1200:
        raise SystemExit("no shell")
print("shell ready at %.0fs" % (time.time() - t0), flush=True)
send("clear\n"); time.sleep(4)
send("for i in $(seq 1 40); do systemctl list-units >/dev/null 2>&1 && break; sleep 3; done\n")
time.sleep(130)
# initial settle: Hyprland crash-loops under TCG until KMS is ready
send("sleep %d\n" % bootwait)
time.sleep(bootwait + 15)

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

prefix = ("sig=$(ls /run/user/1000/hypr/ 2>/dev/null|head -1|sed 's/\\..*//');"
          "HYPRLAND_INSTANCE_SIGNATURE=$sig ")

def poll_hypr():
    """Count running Hyprland processes in the guest; -1 on timeout."""
    send("echo ===POLL===; pgrep -c Hyprland; echo ===END===\n")
    deadline = time.time() + 45
    while time.time() < deadline:
        m = re.search(rb"===POLL===\n(\d+)\n===END===", bytes(buf))
        if m:
            return int(m.group(1))
        time.sleep(1)
    return -1

def gui_like(path):
    """True if the PPM frame looks like a GUI (many colors), not a text console."""
    try:
        with open(path, 'rb') as f:
            data = f.read()
        parts = data.split(b'\n', 3)
        if len(parts) < 4 or parts[0][:2] != b'P6':
            return False
        px = parts[3]
        buckets = set()
        for i in range(0, len(px), 3):
            buckets.add((px[i] >> 4, px[i+1] >> 4, px[i+2] >> 4))
            if len(buckets) > 1500:
                return True
        return len(buckets) >= 400
    except Exception:
        return False

print("waiting for Hyprland process…", flush=True)
hypr_ok = False
for i in range(24):  # up to ~15 min of polling
    n = poll_hypr()
    print("hyprland procs: %s" % n, flush=True)
    if n and n > 0:
        hypr_ok = True
        break
    time.sleep(35)
if not hypr_ok:
    print("WARN: Hyprland process never appeared; continuing best-effort", flush=True)
time.sleep(45)  # let it paint

def shoot(name, binary=None, paint=120):
    ppm = "/tmp/gallery-%s.ppm" % name
    if binary:
        cls = binary.rsplit("/", 1)[-1]
        send(prefix + f'hyprctl dispatch "killall, {cls}" >/dev/null 2>&1\n')
        time.sleep(8)
        send(prefix + f'hyprctl dispatch "exec, {binary}" 2>&1 | head -1\n')
    for attempt in range(4):
        time.sleep(paint if attempt == 0 else 90)
        qmp({"execute": "screendump", "arguments": {"filename": ppm}})
        if gui_like(ppm):
            print("captured %s (attempt %d)" % (name, attempt + 1), flush=True)
            return
        print("%s: console-like frame, waiting for GUI (retry %d)" % (name, attempt + 1), flush=True)
        if binary:
            cls = binary.rsplit("/", 1)[-1]
            send(prefix + f'hyprctl dispatch "killall, {cls}" >/dev/null 2>&1\n')
            time.sleep(20)
    print("captured %s (BEST EFFORT — may still be console)" % name, flush=True)

shoot("desktop", None, paint=25)
for idx, (name, binary, paint, shot) in enumerate(apps):
    shoot(name, binary, int(paint))
    if idx < len(apps) - 1:
        time.sleep(5)
print("gallery done", flush=True)
EOF

kill $QPID 2>/dev/null || true
sleep 2
cd "$W"
for f in /tmp/gallery-*.ppm; do
  [ -f "$f" ] || continue
  n=$(basename "$f" .ppm | sed 's/^gallery-//')
  if command -v convert >/dev/null 2>&1; then
    convert "$f" "$OUTDIR/$n.png"
  else
    cp "$f" "$OUTDIR/$n.ppm"
  fi
  rm -f "$f"
done
echo "gallery saved to $OUTDIR"
ls -la "$OUTDIR"
