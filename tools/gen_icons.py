#!/usr/bin/env python3
"""SimorghOS — unified SVG icon set generator.

Every icon is drawn with the SAME visual grammar:
  * 48x48 viewBox, 24px safe area
  * stroke-based geometry, stroke-width 3, rounded caps & joins
  * one shared teal→gold gradient stroke (+ optional lapis accent fill)
  * no emoji, no raster, no text
Output: config/includes.chroot/usr/share/icons/Simorgh/ (full icon theme)
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "config", "includes.chroot",
                   "usr", "share", "icons", "Simorgh")

HEAD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{s}" height="{s}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#5eead4"/><stop offset=".55" stop-color="#38bdf8"/>
<stop offset="1" stop-color="#f0c46a"/></linearGradient></defs>
<g fill="none" stroke="url(#g)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
{body}
</g></svg>
"""

# Each icon: list of SVG primitives (stroke grammar). Accent fills use fill="url(#g)" opacity .18
ICONS = {
    # ── core apps ────────────────────────────────────────────────
    "terminal": ['<rect x="7" y="9" width="34" height="30" rx="6"/>',
                 '<path d="M14 19l6 5-6 5"/>', '<path d="M24 30h10"/>'],
    "task-manager": ['<rect x="8" y="8" width="32" height="32" rx="7"/>',
                     '<path d="M15 29v-6"/><path d="M22 29V17"/><path d="M29 29v-9"/><path d="M36 29V21" transform="translate(-3 0)"/>'],
    "monitor": ['<path d="M8 34c4 0 5-16 9-16s5 10 8 10 4-14 7-14 4 8 8 8"/>',
                '<rect x="6" y="8" width="36" height="32" rx="6"/>'],
    "screenshot": ['<rect x="7" y="12" width="34" height="26" rx="5"/>',
                   '<circle cx="24" cy="25" r="7"/>', '<path d="M17 12l3-5h8l3 5"/>'],
    "recorder": ['<circle cx="24" cy="24" r="15"/>', '<circle cx="24" cy="24" r="6" fill="url(#g)" stroke="none"/>'],
    "calculator": ['<rect x="11" y="7" width="26" height="34" rx="6"/>',
                   '<path d="M17 15h14"/>', '<path d="M18 25h.1M24 25h.1M30 25h.1M18 32h.1M24 32h.1M30 32h.1"/>'],
    "calendar": ['<rect x="7" y="10" width="34" height="30" rx="6"/>',
                 '<path d="M7 19h34"/><path d="M16 7v6M32 7v6"/>',
                 '<path d="M16 27h.1M24 27h.1M32 27h.1M16 33h.1M24 33h.1"/>'],
    "clock": ['<circle cx="24" cy="24" r="16"/>', '<path d="M24 15v9l6 4"/>'],
    "photos": ['<rect x="7" y="9" width="34" height="30" rx="6"/>',
               '<circle cx="17" cy="19" r="3.5"/>', '<path d="M7 33l10-9 8 7 7-6 9 8"/>'],
    "music": ['<path d="M18 34V14l16-4v20"/>', '<circle cx="14" cy="34" r="4.5"/>', '<circle cx="30" cy="30" r="4.5"/>'],
    "video": ['<rect x="6" y="11" width="36" height="26" rx="6"/>', '<path d="M21 18l10 6-10 6z"/>'],
    "text-editor": ['<path d="M12 8h16l8 8v24a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4z"/>',
                    '<path d="M28 8v8h8"/>', '<path d="M15 24h18M15 30h18M15 36h10"/>'],
    "pdf": ['<path d="M12 6h16l8 8v26a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4V10a4 4 0 0 1 4-4z"/>',
            '<path d="M28 6v8h8"/>', '<path d="M16 30h4a3 3 0 0 0 0-6h-4v12"/>'],
    "mail": ['<rect x="6" y="10" width="36" height="28" rx="6"/>', '<path d="M8 14l16 12 16-12"/>'],
    "security": ['<path d="M24 6l14 5v10c0 10-6 17-14 21-8-4-14-11-14-21V11z"/>', '<path d="M18 23l4.5 5L31 18"/>'],
    "user": ['<circle cx="24" cy="17" r="8"/>', '<path d="M9 40c2-9 8-13 15-13s13 4 15 13"/>'],
    "power": ['<path d="M24 8v14"/>', '<path d="M15 14a14 14 0 1 0 18 0"/>'],
    "update": ['<path d="M38 24a14 14 0 1 1-5-10.8"/>', '<path d="M38 8v7h-7"/>'],
    "installer": ['<path d="M24 8v18"/><path d="M16 18l8 8 8-8"/>',
                  '<path d="M10 30v6a4 4 0 0 0 4 4h20a4 4 0 0 0 4-4v-6"/>'],
    "repair": ['<path d="M28 10a8 8 0 0 0-9 11L9 31a4 4 0 1 0 6 6l10-10a8 8 0 0 0 11-9l-5 5-5-1-1-5z"/>'],
    "restore": ['<path d="M10 24a14 14 0 1 0 4-9.8"/>', '<path d="M10 8v7h7"/>', '<path d="M24 17v7l5 4"/>'],
    "reset": ['<path d="M38 24a14 14 0 1 1-5-10.8"/>', '<path d="M38 8v7h-7"/>', '<circle cx="24" cy="24" r="4"/>'],
    "backup": ['<path d="M14 34a8 8 0 0 1 1-16 10 10 0 0 1 19-2 8 8 0 0 1 0 18z"/>',
               '<path d="M24 26v10"/><path d="M20 32l4 4 4-4"/>'],
    "boot": ['<circle cx="24" cy="24" r="7"/>',
             '<path d="M24 6v6M24 36v6M6 24h6M36 24h6M11 11l4 4M33 33l4 4M37 11l-4 4M15 33l-4 4"/>'],
    "accessibility": ['<circle cx="24" cy="10" r="4"/>', '<path d="M10 18c9 3 19 3 28 0"/>',
                      '<path d="M24 20v10l-7 12M24 30l7 12"/>'],
    "developer": ['<path d="M16 16l-9 8 9 8"/>', '<path d="M32 16l9 8-9 8"/>', '<path d="M27 10l-6 28"/>'],
    "about": ['<circle cx="24" cy="24" r="17"/>', '<path d="M24 22v10"/>', '<path d="M24 15h.1"/>'],
    # ── universal UI glyphs ─────────────────────────────────────
    "home": ['<path d="M9 22L24 9l15 13"/>', '<path d="M13 20v17a3 3 0 0 0 3 3h16a3 3 0 0 0 3-3V20"/>'],
    "files": ['<path d="M7 14a4 4 0 0 1 4-4h8l4 5h14a4 4 0 0 1 4 4v15a4 4 0 0 1-4 4H11a4 4 0 0 1-4-4z"/>'],
    "settings": ['<circle cx="24" cy="24" r="6"/>',
                 '<path d="M24 7v5M24 36v5M7 24h5M36 24h5M12 12l3.5 3.5M32.5 32.5L36 36M36 12l-3.5 3.5M15.5 32.5L12 36"/>'],
    "search": ['<circle cx="21" cy="21" r="11"/>', '<path d="M29 29l10 10"/>'],
    "browser": ['<circle cx="24" cy="24" r="16"/>', '<path d="M8 24h32"/>',
                '<path d="M24 8c-6 5-6 27 0 32M24 8c6 5 6 27 0 32"/>'],
    "trash": ['<path d="M10 14h28"/>', '<path d="M18 14V9a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v5"/>',
              '<path d="M14 14l2 24a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4l2-24"/>', '<path d="M20 21v14M28 21v14"/>'],
    "edit": ['<path d="M30 8l10 10-22 22H8V30z"/>', '<path d="M26 12l10 10"/>'],
    "share": ['<circle cx="14" cy="24" r="5"/>', '<circle cx="34" cy="12" r="5"/>', '<circle cx="34" cy="36" r="5"/>',
              '<path d="M18.5 21.5l11-7M18.5 26.5l11 7"/>'],
    "copy": ['<rect x="16" y="16" width="24" height="24" rx="5"/>', '<path d="M32 12V10a4 4 0 0 0-4-4H12a4 4 0 0 0-4 4v16a4 4 0 0 0 4 4h2"/>'],
    "cut": ['<circle cx="14" cy="14" r="5"/>', '<circle cx="14" cy="34" r="5"/>', '<path d="M18 17l20 17M18 31l20-17"/>'],
    "paste": ['<rect x="10" y="10" width="28" height="30" rx="5"/>', '<path d="M19 10a5 5 0 0 1 10 0"/>',
              '<path d="M17 22h14M17 29h14"/>'],
    "refresh": ['<path d="M38 24a14 14 0 1 1-5-10.8"/>', '<path d="M38 8v7h-7"/>'],
    "back": ['<path d="M29 10L15 24l14 14"/>'],
    "forward": ['<path d="M19 10l14 14-14 14"/>'],
    "close": ['<path d="M13 13l22 22M35 13L13 35"/>'],
    "menu": ['<path d="M10 15h28M10 24h28M10 33h28"/>'],
    "more": ['<path d="M13 24h.1M24 24h.1M35 24h.1"/>'],
    "download": ['<path d="M24 8v20"/><path d="M15 20l9 9 9-9"/>', '<path d="M10 34v4a4 4 0 0 0 4 4h20a4 4 0 0 0 4-4v-4"/>'],
    "upload": ['<path d="M24 28V8"/><path d="M15 17l9-9 9 9"/>', '<path d="M10 34v4a4 4 0 0 0 4 4h20a4 4 0 0 0 4-4v-4"/>'],
}

INDEX_APPS = {
    "terminal": "utilities-terminal", "task-manager": "utilities-system-monitor",
    "monitor": "utilities-system-monitor", "screenshot": "applets-screenshooter",
    "recorder": "media-record", "calculator": "accessories-calculator",
    "calendar": "x-office-calendar", "clock": "preferences-system-time",
    "photos": "multimedia-photo-manager", "music": "multimedia-audio-player",
    "video": "multimedia-video-player", "text-editor": "accessories-text-editor",
    "pdf": "x-office-pdf", "mail": "mail-message", "security": "security-high",
    "user": "system-users", "power": "system-shutdown", "update": "system-software-update",
    "installer": "system-installer", "repair": "preferences-system-repair",
    "restore": "document-revert", "reset": "view-refresh", "backup": "document-save",
    "boot": "system-boot", "accessibility": "preferences-desktop-accessibility",
    "developer": "applications-engineering", "about": "help-about",
    "home": "go-home", "files": "system-file-manager", "settings": "preferences-system",
    "search": "edit-find", "browser": "web-browser", "trash": "user-trash",
    "edit": "accessories-text-editor", "share": "emblem-shared", "copy": "edit-copy",
    "cut": "edit-cut", "paste": "edit-paste", "refresh": "view-refresh",
    "back": "go-previous", "forward": "go-next", "close": "window-close",
    "menu": "open-menu", "more": "view-more", "download": "document-save",
    "upload": "document-send",
}


def main():
    apps = os.path.join(OUT, "apps", "scalable")
    actions = os.path.join(OUT, "actions", "scalable")
    for d in (apps, actions):
        os.makedirs(d, exist_ok=True)
    for name, body in ICONS.items():
        svg = HEAD.format(s=48, body="\n".join(body))
        target = apps if name in INDEX_APPS and name in (
            "terminal", "task-manager", "monitor", "screenshot", "recorder", "calculator",
            "calendar", "clock", "photos", "music", "video", "text-editor", "pdf", "mail",
            "security", "user", "power", "update", "installer", "repair", "restore", "reset",
            "backup", "boot", "accessibility", "developer", "about", "home", "files",
            "settings", "search", "browser", "trash") else actions
        with open(os.path.join(target, f"{name}.svg"), "w") as f:
            f.write(svg)
        # 48px & 96px rendered copies for panels/launchers
        for size in (48, 96):
            with open(os.path.join(target, f"{name}.svg"), "r") as f:
                data = f.read()
            _ = size  # scalable only; GTK scales
    # index.theme so it is a real icon theme
    with open(os.path.join(OUT, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=Simorgh\nInherits=Papirus-Dark,breeze,Adwaita\n"
                "Directories=" + ",".join(sorted({
                    os.path.relpath(d, OUT) for d in (apps, actions)})) + "\n\n")
        for d in (apps, actions):
            rel = os.path.relpath(d, OUT)
            f.write(f"[{rel}]\nSize=48\nType=Scalable\nMinSize=16\nMaxSize=512\n\n")
    # symlinks for freedesktop standard names
    linkdir = apps
    for name, std in INDEX_APPS.items():
        if name in ICONS:
            src = os.path.join(linkdir, f"{name}.svg")
            dst = os.path.join(linkdir, f"{std}.svg")
            if os.path.exists(src) and not os.path.lexists(dst):
                os.symlink(os.path.basename(src), dst)
    print(f"icons written: {len(ICONS)} + {len(INDEX_APPS)} aliases")


if __name__ == "__main__":
    main()
