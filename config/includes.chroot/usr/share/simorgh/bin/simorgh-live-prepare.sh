#!/bin/sh
# SimorghOS — live boot preparation.
# Mask LightDM on live media so multi-user.target does not wait for it
# (its Type=notify start can take extremely long under software rendering).
set -e

# Drop LightDM out of the boot path.
ln -sf /dev/null /etc/systemd/system/lightdm.service 2>/dev/null || true
rm -f /etc/systemd/system/multi-user.target.wants/lightdm.service 2>/dev/null || true
rm -f /etc/systemd/system/display-manager.service 2>/dev/null || true
systemctl daemon-reload 2>/dev/null || true

# QA boot flags (used by the screenshot automation):
#   simorgh-shot=calamares  / simorgh-shot=simorgh-<app>
# Hyprland reads /etc/xdg/autostart and ~/.config/autostart; the live root
# is read-only, so write to the user's home when possible.
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
