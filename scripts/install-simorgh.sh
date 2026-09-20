#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  سیمرغ‌اواس — تبدیل دبیان ۱۳ موجود به سیمرغ
#  کاربرد: sudo ./scripts/install-simorgh.sh
# ─────────────────────────────────────────────────────────────
set -euo pipefail

if [[ $EUID -ne 0 ]]; then echo "نیازمند sudo" >&2; exit 1; fi
. /etc/os-release
if [[ "${VERSION_CODENAME:-}" != "trixie" ]]; then
    echo "سیمرغ فقط روی Debian 13 (trixie) نصب می‌شود؛ شما: ${VERSION_CODENAME:-نامشخص}" >&2
    exit 1
fi

echo "── فعال‌سازی backports ──"
if [[ ! -f /etc/apt/sources.list.d/simorgh-backports.sources ]]; then
cat > /etc/apt/sources.list.d/simorgh-backports.sources <<'EOF'
Types: deb
URIs: http://deb.debian.org/debian
Suites: trixie-backports
Components: main contrib non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.pgp
EOF
fi

cat > /etc/apt/preferences.d/simorgh-hypr.pref <<'EOF'
Package: hyprland hyprland-guiutils hyprpaper hyprlock hypridle hyprpolkitagent xdg-desktop-portal-hyprland libxkbcommon0 libxkbregistry0
Pin: release a=stable-backports
Pin-Priority: 500
EOF

apt-get update

echo "── نصب پشتهٔ سیمرغ ──"
install -d /usr/share/keyrings
cp -f "$ROOT"/config/includes.chroot_before_packages/usr/share/simorgh/brave-keyring.gpg /usr/share/keyrings/brave-browser-archive-keyring.gpg
cat > /etc/apt/sources.list.d/brave.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com stable main
EOF
apt-get update

apt-get install -y -t trixie-backports \
    hyprland hyprland-guiutils hyprpaper hyprlock hypridle hyprpolkitagent \
    xdg-desktop-portal-hyprland \
    waybar kitty rofi mako-notifier cliphist grim slurp wl-clipboard wlogout \
    light brightnessctl playerctl pamixer \
    pipewire pipewire-pulse wireplumber pavucontrol \
    network-manager-gnome gvfs gvfs-backends thunar tumbler file-roller \
    evince mpv geany micro fastfetch \
    brave-browser flatpak timeshift gammastep wf-recorder \
    power-profiles-daemon unattended-upgrades \
    firefox-esr firefox-esr-l10n-fa \
    fonts-vazirmatn fonts-vazirmatn-variable fonts-noto-color-emoji fonts-firacode \
    orchis-gtk-theme papirus-icon-theme breeze-cursor-theme \
    nwg-look qt6ct xsettingsd lightdm slick-greeter \
    jcal fcitx5 myspell-fa aspell-fa calamares
update-alternatives --set x-www-browser /usr/bin/brave-browser || true
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo || true

echo "── کپی تنظیمات سیمرغ ──"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
install -d /usr/share/simorgh/bin
cp -r "$ROOT"/config/includes.chroot/usr/share/simorgh/. /usr/share/simorgh/
cp -r "$ROOT"/config/includes.chroot/usr/share/backgrounds /usr/share/
cp -r "$ROOT"/config/includes.chroot/usr/share/pixmaps /usr/share/
cp -r "$ROOT"/config/includes.chroot/usr/share/grub /usr/share/
cp -r "$ROOT"/config/includes.chroot/usr/share/plymouth /usr/share/
cp -r "$ROOT"/config/includes.chroot/usr/share/wayland-sessions /usr/share/
cp -r "$ROOT"/config/includes.chroot/usr/share/applications/simorgh-*.desktop /usr/share/applications/
cp -r "$ROOT"/config/includes.chroot/etc/fonts/local.conf /etc/fonts/
cp -r "$ROOT"/config/includes.chroot/etc/xsettingsd /etc/
cp -r "$ROOT"/config/includes.chroot/etc/wlogout /etc/
mkdir -p /etc/calamares
cp -r "$ROOT"/config/includes.chroot/etc/calamares/. /etc/calamares/
cp -r "$ROOT"/config/includes.chroot/etc/lightdm/. /etc/lightdm/
chmod -R +x /usr/share/simorgh/bin

for u in /root /home/*; do
    [[ -d "$u" ]] || continue
    mkdir -p "$u/.config"
    cp -rn "$ROOT"/config/includes.chroot/etc/skel/.config/. "$u/.config/" || true
done

echo "── locale و سرویس‌ها ──"
sed -i 's/^# *fa_IR.*/fa_IR.UTF-8 UTF-8/' /etc/locale.gen
locale-gen || true
ln -sf /usr/lib/systemd/system/lightdm.service /etc/systemd/system/display-manager.service
systemctl enable NetworkManager 2>/dev/null || true

echo "✔ سیمرغ آماده است؛ از LightDM نشست «سیمرغ (Hyprland)» را برگزینید."
