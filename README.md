# SimorghOS

SimorghOS (سیمرغ) is an independent desktop operating system. Persian (فارسی) documentation: [README.fa.md](README.fa.md)

![Desktop](docs/screenshots/desktop.png)

---

## 1. Create a bootable USB

Download `simorgh-os-0.0.1-amd64.iso` from [Releases](../../releases) and verify it:

```bash
sha256sum -c simorgh-os-0.0.1-amd64.iso.sha256
```

Write it to a USB stick (replace `sdX` with your drive — `lsblk` shows it):

```bash
sudo dd if=simorgh-os-0.0.1-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

Or use balenaEtcher / Ventoy / Rufus (DD mode).

## 2. Boot and install

1. Boot from the USB (UEFI or BIOS). The live desktop starts by itself.
2. On first start, **Setup** opens: choose interface language (English / فارسی), calendar (Jalali / Gregorian / both) and theme.
3. Double-click **Install SimorghOS** (Calamares) → language → keyboard → partition (erase disk or manual) → user → finish → reboot without the USB.

Dual-boot: choose *manual partitioning* in the installer and pick free space; GRUB lists the other OS.

## 3. First-run tour

| Action | How |
|---|---|
| Open apps (launcher) | `Super` + `D` |
| Switch EN ↔ FA keyboard | `Super` + `Space` |
| Control Center (language, calendar, theme, wallpaper) | `Super` + `C` |
| App Center (curated + Flathub) | `Super` + `A` |
| Terminal | `Super` + `Return` |
| File manager | `Super` + `E` |
| Browser (Brave) | `Super` + `W` |
| Screenshot / area | `Print` / `Super`+`Shift`+`S` |
| Clipboard history | `Super` + `Shift` + `V` |
| Lock screen | `Super` + `L` |
| Power menu | `Super` + `M` |
| Workspaces | `Super` + `1..9`, move window with `Super`+`Shift`+`1..9` |

## 4. Everyday commands

Everything goes through one hub — `simorgh`:

```text
simorgh update                    upgrade apt + flatpak
simorgh install vlc               install anything (Debian repo or Flathub, auto-detected)
simorgh install org.gimp.GIMP     install by Flatpak app-id
simorgh remove  vlc
simorgh search  editor
simorgh restore                   Timeshift restore points (create/list/restore)
simorgh info                      system summary

simorgh lang fa                   switch interface to Persian (en to switch back; re-login applies)
simorgh theme lapis               themes: dark | lapis | light
simorgh calendar jalali           calendar: jalali | gregorian | both
simorgh wallpaper list            show bundled wallpapers
simorgh wallpaper /path/to/img    set any image as wallpaper
simorgh center                    Control Center menu
simorgh store                     App Center menu

simorgh date                      today in Jalali (simorgh date --short / --latin)
simorgh screenshot                save a screenshot
simorgh screenshot area           screenshot a selected region
simorgh record start | stop       record the screen (wf-recorder)
simorgh clipboard                 pick from clipboard history

simorgh apps                      list every core app
simorgh open files                launch any app by name
simorgh files|settings|store|power|usb|scan|tweaks|notes|videos|downloads|backup|archive|fonts|services
```

The desktop ships 30+ native apps (Files, Settings, Store, Power, USB Creator,
Scanner, Tweaks, Notes, Videos, Photos, Music, Downloads, Backup, Archives,
Fonts, Services, Calendar, Clock, Screenshot, Recorder, Security, Update,
Recovery, Accessibility, Developer, User, Mail, Welcome, …) — the full
catalogue with exact commands: [docs/APPS.md](docs/APPS.md) ·
[APPS-fa.md](docs/APPS-fa.md).

Standalone equivalents (same tools, direct): `simorgh-setup`, `simorgh-lang en|fa`,
`simorgh-set-theme dark|lapis|light`, `simorgh-jdate [--short|--waybar|--latin]`,
`simorgh-app install|remove|search|browse`.

## 5. Add anything you like

The system is yours to extend:

```bash
simorgh install <name>        # apt package or Flathub app, one command
simorgh store                 # graphical App Center (Flathub wired in)
flatpak install flathub <id>  # any Flathub app directly
sudo apt install <pkg>        # any Debian package directly
```

Custom commands: drop any executable in `~/.config/simorgh/plugins/` — it instantly
becomes `simorgh <name>`. Example:

```bash
echo '#!/bin/sh
flatpak run org.telegram.desktop' > ~/.config/simorgh/plugins/telegram
chmod +x ~/.config/simorgh/plugins/telegram
simorgh telegram      # works
```

## 6. Keyboard layout (Persian)

`Super` + `Space` switches US ↔ Persian (fcitx5). Layout indicator sits in the bar.

## 7. Restore points and updates

```bash
simorgh restore               # create, list or restore snapshots (Timeshift)
simorgh update                # full upgrade
```

Security updates are applied automatically in the background (can be changed in
`/etc/apt/apt.conf.d/20simorgh-autoupgrade`).

## 8. Configuration files

| File | Purpose |
|---|---|
| `~/.config/simorgh/prefs` | calendar, digits, theme |
| `~/.config/simorgh/lang` | per-user interface language |
| `~/.config/hypr/*.conf` | compositor, keybindings, lock, idle, wallpaper |
| `~/.config/waybar/*` | the bar |
| `~/.config/rofi/*` | launcher / menus |
| `/etc/simorgh/defaults` | system-wide defaults |

## 9. Building from source

The official ISO is built by GitHub Actions (`.github/workflows/build-iso.yml`) on
every `v*` tag. To build locally on Debian 13:

```bash
sudo apt install live-build xorriso squashfs-tools dosfstools mtools rsync debootstrap figlet
sudo -E ./build.sh          # → dist/simorgh-os-0.0.1-amd64.iso
```

Testing without hardware:

```bash
qemu-system-x86_64 -m 2048 -cdrom dist/simorgh-os-0.0.1-amd64.iso
```

## 10. More reading

- [Application suite (English)](docs/APPS.md)
- [Application suite (Persian)](docs/APPS-fa.md)
- [Installation guide (Persian)](docs/INSTALL-fa.md)
- [Keyboard & Persian input (Persian)](docs/KEYBOARD-fa.md)
- [Theming (Persian)](docs/THEME-fa.md)

Issues and requests: [github.com/ZALPRO/SimorghOS/issues](../../issues)
