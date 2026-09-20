# SimorghOS 0.0.1 — Application Suite

Every command below is exact. Apps open from the launcher (Super key), the
right-click desktop menu, or the terminal.

## Opening any app

```bash
simorgh apps                     # list every core app
simorgh open files               # launch it by name (no "simorgh-" prefix)
```

Or press **Super** and type the app name.

---

## Files

File manager: places, USB devices, trash, history, sort, filter, clipboard,
rename (F2), new folder, properties, move-to-trash (Delete).

```bash
simorgh files
xdg-open ~/Downloads             # open a folder in Files
```

## Settings

Unified panel: appearance (theme, wallpaper, accent), display (resolution,
scale, refresh), sound, network, keyboard, time zone, about.

```bash
simorgh settings
```

## Store

Three catalogues in one window: Simorgh core apps, Flatpak (Flathub), and APT.
Search filters all three; Install uses `pkexec` when root is required.

```bash
simorgh store                    # the GTK store
simorgh appcenter                # one-click Flathub picker (terminal menu)
simorgh install vlc              # apt
simorgh install org.videolan.VLC # Flathub (auto-detected by ID)
```

## Power

Lock, sleep, suspend, restart, shutdown.

```bash
simorgh power
systemctl suspend                # same from the terminal
```

## USB Creator

Write any ISO to a USB drive with progress and optional SHA-256 verification.

```bash
simorgh usb
# or the classic way:
sudo dd if=simorgh-os-0.0.1-amd64.iso of=/dev/sdX bs=4M conv=fsync
sha256sum -c simorgh-os-0.0.1-amd64.iso.sha256
```

## Scanner

SANE front-end: device, color/gray/lineart, 72–1200 DPI, PNG/JPEG/PDF,
multi-page PDF appending, preview before saving to `~/Pictures/Scans`.

```bash
simorgh scan
scanimage --list                 # what the OS sees
```

## Tweaks

Live Hyprland appearance: borders, blur, shadows, rounding, gaps, animation
speed, window scale, layout. Every change applies instantly; Reset restores
Simorgh defaults.

```bash
simorgh tweaks
hyprctl keyword gaps:inner = 8   # the same thing from the terminal
```

## Notes

Markdown notes in `~/Notes`: folders, search, pin, export, autosave,
soft-delete (`~/Notes/Trash`).

```bash
simorgh notes
```

## Videos

Library of `~/Videos`: thumbnails (ffmpeg), duration + resolution (ffprobe),
search, double-click to play in mpv.

```bash
simorgh videos
mpv ~/Videos/clip.mp4
```

## Photos

Library of `~/Pictures`: grid, search, albums, favorites, recent; viewer with
rotate, crop, filters, EXIF, save-as.

```bash
simorgh photos
```

## Music

Library of `~/Music`: search, queue, playlists (saved to
`~/.config/simorgh/playlists.json`), transport controls, volume — all driven
through mpv's IPC socket.

```bash
simorgh music
```

## Downloads

aria2-powered queue manager: paste URLs (or Paste), parallel connections,
retry, stop-all, recent-files list with sizes. Downloads land in `~/Downloads`.

```bash
simorgh downloads
aria2c "https://example.com/file.zip"   # standalone equivalent
```

## Backup

Timeshift snapshots (system or system+home), browse + restore, and one-click
file archives of `~/Documents ~/Pictures ~/Downloads ~/Notes` into
`~/Backups/*.tar.gz`.

```bash
simorgh backup
sudo timeshift --create --comments "before upgrade"
ls /run/timeshift/backup
```

## Archives

Open zip/tar/tar.gz, browse entries, extract all or one entry, and create
new zip/tar.gz from a folder.

```bash
simorgh archive ~/Downloads/zip.zip
tar -xzf file.tar.gz              # terminal equivalent
```

## Fonts

List installed fonts with live preview, install `.ttf/.otf` into
`~/.local/share/fonts` (user scope, no root needed).

```bash
simorgh fonts
fc-list | grep -i vazir
```

## Services

Toggle session autostart entries (`~/.config/autostart` +
`/etc/xdg/autostart`) and manage `systemctl --user` units (start/stop/restart,
status colors).

```bash
simorgh services
systemctl --user list-units --type=service
```

## Welcome

First-boot wizard: language, time zone, keyboard layout (US+Persian with
Super+Space), optional LibreOffice/Thunderbird/VLC install. Runs once
(marker `~/.config/simorgh/.welcomed`).

```bash
simorgh welcome --force          # re-run the wizard
```

---

## System tools (from 0.0.1 core)

| App | Opens with | What it does |
|---|---|---|
| Terminal | `simorgh-terminal` (kitty) | Wayland terminal, themed |
| Task Monitor | `simorgh-monitor` (gnome-system-monitor) | CPU/RAM/processes |
| Calculator | `simorgh-calc` | gnome-calculator |
| Text Editor | `simorgh-editor` (geany) | lightweight code editor |
| PDF Viewer | `simorgh-pdf` (evince) | documents |
| Screenshot | `simorgh-shot` | full / window / area, copy / save / share |
| Recorder | `simorgh-rec` | screen + mic to `~/Videos` |
| Calendar | `simorgh-calendar` | Jalali + Gregorian dual grid, events |
| Clock | `simorgh-clock` | world clock, alarms, timer, stopwatch |
| Security | `simorgh-security` | firmware (fwupd), firewall, LUKS, privacy |
| Update | `simorgh-update-gui` | apt upgrade with progress + upgradable list |
| Recovery | `simorgh-recovery` | repair dpkg/apt, snapshots, boot options, reset |
| Accessibility | `simorgh-access` | reduce motion, color filter, pointer, key repeat |
| Developer | `simorgh-dev` | toolchain install, logs (kitty + journalctl), btop |
| User | `simorgh-user` | profile, password, accounts, lock, logout |
| Mail | `simorgh-mail` | opens Thunderbird or offers one-click install |
| About | `simorgh-about` | system summary + branding |
| Center | `simorgh-center` | hub menu for every system tool |
| Installer | `simorgh-install` (Calamares) | partitioning, user, boot loader |

## The `simorgh` hub

```bash
simorgh update                   # apt full-upgrade + flatpak update
simorgh search <query>           # apt + Flathub
simorgh restore                  # Timeshift GUI
simorgh info                     # fastfetch
simorgh lang en|fa               # UI language
simorgh theme dark|lapis|light   # global theme (hyprland+waybar+gtk+qt)
simorgh calendar jalali|gregorian|both
simorgh wallpaper list|<file>
simorgh date                     # Jalali date
simorgh screenshot [area]
simorgh record start|stop
simorgh clipboard                # history picker
simorgh plugins                  # list plugins
simorgh nightlight on|off        # plugin: night light
simorgh wall                     # plugin: wallpaper picker
simorgh vol up|down|mute         # plugin: volume
simorgh mem                      # plugin: RAM/disk summary
simorgh shot                     # plugin: area shot → clipboard
```

Plugins: any executable dropped into `~/.config/simorgh/plugins/` becomes
`simorgh <name>`.
