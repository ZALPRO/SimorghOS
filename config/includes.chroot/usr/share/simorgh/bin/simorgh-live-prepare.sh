#!/bin/sh
# SimorghOS — live boot preparation (no unit changes, no daemon-reload).
# Writes the QA autostart entry when a simorgh-shot= boot flag is present.
set -e

# QA boot flags (used by the screenshot automation):
#   simorgh-shot=calamares  /  simorgh-shot=simorgh-<app>
# Hyprland reads /etc/xdg/autostart and ~/.config/autostart.
flag=$(sed -n 's/.*simorgh-shot=\([^ ]*\).*/\1/p' /proc/cmdline | head -1) || true
if [ -n "${flag:-}" ]; then
    name=$flag
    [ "$flag" = calamares ] && name=installer
    for d in /home/user/.config/autostart /etc/xdg/autostart; do
        mkdir -p "$d" 2>/dev/null || continue
        printf '[Desktop Entry]\nType=Application\nName=QA %s\nExec=sh -c "sleep 10; %s"\nX-GNOME-Autostart-enabled=true\n' \
            "$name" "$flag" > "$d/simorgh-qa-$name.desktop" 2>/dev/null || true
    done
fi
exit 0
