#!/usr/bin/env python3
"""SimorghOS — unified icon family (filled, glass-tile).

Design language — one consistent family, no emoji, no raster, no text:
  * 48x48 grid, 2px safe margin
  * every icon sits on the SAME dark "glass" tile (rounded, subtle top scene,
    faint brand glow at the base) so the launcher reads as one premium set
  * the glyph itself is FILLED with the brand teal→blue gradient, with gold
    accents and off-white highlights for depth — the look Pop/Fedora/NixOS use
  * two tones (brand gradient + a darker under-shade) give the glyphs volume

Run `python3 tools/gen_icons.py` to regenerate everything into the chroot.
Run `python3 tools/gen_icons.py --sheet out.png` to render a contact sheet.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "config", "includes.chroot", "usr", "share", "icons", "Simorgh")

# ── palette ────────────────────────────────────────────────────────────────
TEAL, BLUE, SKY = "#5eead4", "#38bdf8", "#7dd3fc"
GOLD, WHITE, INK = "#f0c46a", "#f1f5f9", "#0b1220"

DEFS = f"""<defs>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1b2740"/><stop offset="1" stop-color="#0b1120"/>
</linearGradient>
<linearGradient id="scene" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.14"/>
  <stop offset="0.14" stop-color="#ffffff" stop-opacity="0.035"/>
  <stop offset="0.55" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.28"/>
  <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.05"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0.10"/>
</linearGradient>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{TEAL}"/><stop offset="0.55" stop-color="{BLUE}"/><stop offset="1" stop-color="{SKY}"/>
</linearGradient>
<linearGradient id="gd" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#2563eb"/>
</linearGradient>
<radialGradient id="glow" cx="0.5" cy="1" r="0.9">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0.30"/>
  <stop offset="0.6" stop-color="{BLUE}" stop-opacity="0.05"/>
  <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
</radialGradient>
</defs>"""

TILE = f"""<rect x="2.5" y="2.5" width="43" height="43" rx="11.5" fill="url(#tile)"/>
<ellipse cx="24" cy="47" rx="26" ry="17" fill="url(#glow)"/>
<rect x="2.5" y="2.5" width="43" height="43" rx="11.5" fill="url(#scene)"/>
<rect x="3.4" y="3.4" width="41.2" height="41.2" rx="10.8" fill="none" stroke="url(#edge)" stroke-width="1.2"/>"""

# Each glyph: list of SVG fragments (fills). Mixed fills/strokes allowed for
# thin detail lines. All coordinates live inside the ~10..38 safe area.
G = "url(#g)"      # brand gradient (primary)
GD = "url(#gd)"    # darker brand (under-shade / depth)
DARK = "#152238"   # inset dark surface
DARK2 = "#1d2c49"  # inset dark surface (lighter)

ICONS = {
    # ── core applications ──────────────────────────────────────────────────
    "terminal": [
        f'<rect x="9" y="11" width="30" height="26" rx="6" fill="{DARK}"/>',
        f'<rect x="9" y="11" width="30" height="7" rx="6" fill="{DARK2}"/>',
        f'<rect x="9" y="15.5" width="30" height="2.5" fill="{DARK}"/>',
        f'<circle cx="13.5" cy="14.5" r="1.4" fill="{GOLD}"/><circle cx="18" cy="14.5" r="1.4" fill="{BLUE}"/>',
        f'<path d="M13.5 22.5l5 4.5-5 4.5" fill="none" stroke="{G}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<rect x="21.5" y="30" width="9" height="2.6" rx="1.3" fill="{WHITE}"/>',
    ],
    "files": [
        f'<path d="M9 15a4 4 0 0 1 4-4h7l4 4h11a4 4 0 0 1 4 4v13a4 4 0 0 1-4 4H13a4 4 0 0 1-4-4z" fill="{GD}"/>',
        f'<path d="M9 19h30v13a4 4 0 0 1-4 4H13a4 4 0 0 1-4-4z" fill="{G}"/>',
        f'<rect x="9" y="18" width="30" height="2.4" fill="#ffffff" opacity="0.18"/>',
    ],
    "home": [
        f'<path d="M24 9l15 13h-4.5v14a3 3 0 0 1-3 3h-15a3 3 0 0 1-3-3V22H9z" fill="{G}"/>',
        f'<path d="M24 9l15 13h-4.5V22H9v0z" fill="#ffffff" opacity="0.14"/>',
        f'<rect x="20.5" y="27" width="7" height="12" rx="1.5" fill="{GOLD}"/>',
    ],
    "browser": [
        f'<circle cx="24" cy="24" r="14.5" fill="{G}"/>',
        f'<ellipse cx="19" cy="18" rx="6" ry="4.5" fill="#ffffff" opacity="0.22"/>',
        f'<path d="M9.5 24h29" fill="none" stroke="{WHITE}" stroke-width="1.8" opacity="0.85"/>',
        f'<path d="M24 9.5c-5.5 4.5-5.5 24.5 0 29M24 9.5c5.5 4.5 5.5 24.5 0 29" fill="none" stroke="{WHITE}" stroke-width="1.8" opacity="0.85"/>',
        f'<ellipse cx="24" cy="24" rx="7" ry="14.5" fill="none" stroke="{WHITE}" stroke-width="1.6" opacity="0.7"/>',
    ],
    "mail": [
        f'<rect x="8" y="12" width="32" height="24" rx="5" fill="{G}"/>',
        f'<path d="M8 17l16 11 16-11" fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-linejoin="round"/>',
        f'<circle cx="35" cy="14" r="4.5" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>',
    ],
    "music": [
        f'<path d="M19 34V15l15-4v19" fill="none" stroke="{G}" stroke-width="3.4" stroke-linejoin="round"/>',
        f'<path d="M19 34V15l15-4v19" fill="none" stroke="#ffffff" stroke-width="0.8" opacity="0.25" stroke-linejoin="round"/>',
        f'<ellipse cx="15.5" cy="34" rx="4.6" ry="4" fill="{G}"/>',
        f'<ellipse cx="30.5" cy="30" rx="4.6" ry="4" fill="{G}"/>',
        f'<path d="M19 18.5h15" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>',
    ],
    "video": [
        f'<rect x="7" y="12" width="34" height="24" rx="6" fill="{DARK2}"/>',
        f'<path d="M20 18.5l11 5.5-11 5.5z" fill="{GOLD}"/>',
        f'<circle cx="12" cy="16" r="1.3" fill="{WHITE}" opacity="0.5"/>',
    ],
    "photos": [
        f'<rect x="8" y="11" width="32" height="26" rx="5.5" fill="{DARK2}"/>',
        f'<circle cx="17" cy="19" r="3.4" fill="{GOLD}"/>',
        f'<path d="M8 32l9-8 7 6 6.5-5.5L40 30v3a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4z" fill="{G}"/>',
        f'<path d="M8 32l9-8 7 6 6.5-5.5L40 30v2H8z" fill="#ffffff" opacity="0.14"/>',
    ],
    "text-editor": [
        f'<path d="M14 9h12l8 8v19a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4V13a4 4 0 0 1 4-4z" fill="{G}"/>',
        f'<path d="M26 9l8 8h-8z" fill="#ffffff" opacity="0.28"/>',
        f'<path d="M15 24h18M15 29h18M15 34h11" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>',
    ],
    "pdf": [
        f'<path d="M14 8h12l8 8v20a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4z" fill="{WHITE}"/>',
        f'<path d="M26 8l8 8h-8z" fill="#cbd5e1"/>',
        f'<rect x="14" y="24" width="20" height="10" rx="2.5" fill="{BLUE}"/>',
        f'<path d="M17 29h4a2.4 2.4 0 0 0 0-4.8h-4v9.6" fill="none" stroke="{WHITE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "calculator": [
        f'<rect x="11" y="9" width="26" height="30" rx="6" fill="{DARK2}"/>',
        f'<rect x="14.5" y="13" width="19" height="7" rx="2" fill="{G}"/>',
        f'<g fill="{WHITE}" opacity="0.9"><rect x="14.5" y="24" width="4.4" height="4.4" rx="1.4"/><rect x="21.8" y="24" width="4.4" height="4.4" rx="1.4"/><rect x="29" y="24" width="4.4" height="4.4" rx="1.4"/><rect x="14.5" y="31.3" width="4.4" height="4.4" rx="1.4"/><rect x="21.8" y="31.3" width="4.4" height="4.4" rx="1.4"/></g>',
        f'<rect x="29" y="31.3" width="4.4" height="4.4" rx="1.4" fill="{GOLD}"/>',
    ],
    "calendar": [
        f'<rect x="8" y="11" width="32" height="27" rx="5.5" fill="{G}"/>',
        f'<rect x="8" y="11" width="32" height="8" rx="5.5" fill="{GD}"/>',
        f'<rect x="8" y="16" width="32" height="3" fill="{G}"/>',
        f'<rect x="15" y="8" width="3" height="7" rx="1.5" fill="{WHITE}"/><rect x="30" y="8" width="3" height="7" rx="1.5" fill="{WHITE}"/>',
        f'<g fill="{WHITE}" opacity="0.92"><rect x="13.5" y="23" width="4.5" height="4.5" rx="1.3"/><rect x="21.8" y="23" width="4.5" height="4.5" rx="1.3"/><rect x="30" y="23" width="4.5" height="4.5" rx="1.3"/><rect x="13.5" y="30" width="4.5" height="4.5" rx="1.3"/></g>',
        f'<rect x="21.8" y="30" width="4.5" height="4.5" rx="1.3" fill="{GOLD}"/>',
    ],
    "clock": [
        f'<circle cx="24" cy="24" r="14.5" fill="{G}"/>',
        f'<circle cx="24" cy="24" r="14.5" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.25"/>',
        f'<path d="M24 14.5V24l6.5 4.5" fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="24" cy="24" r="1.8" fill="{GOLD}"/>',
    ],
    "screenshot": [
        f'<rect x="8" y="12" width="32" height="24" rx="5.5" fill="{DARK2}"/>',
        f'<path d="M14 24a8 8 0 0 1 8-8" fill="none" stroke="{G}" stroke-width="2.6" stroke-linecap="round"/>',
        f'<path d="M34 24a8 8 0 0 1-8 8" fill="none" stroke="{G}" stroke-width="2.6" stroke-linecap="round"/>',
        f'<path d="M14 16.5v4M12 18.5h4M34 31.5v4M32 33.5h4M34 21.5v4M32 23.5h4M14 26.5v4M12 28.5h4" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round"/>',
    ],
    "recorder": [
        f'<rect x="8" y="14" width="21" height="20" rx="5" fill="{G}"/>',
        f'<path d="M29 20l10-5v18l-10-5z" fill="{GD}"/>',
        f'<circle cx="18.5" cy="24" r="5.5" fill="{INK}" opacity="0.35"/>',
        f'<circle cx="18.5" cy="24" r="3.4" fill="{GOLD}"/>',
    ],
    "task-manager": [
        f'<g fill="{G}"><rect x="12" y="27" width="5" height="8" rx="2"/><rect x="21.5" y="20" width="5" height="15" rx="2"/><rect x="31" y="14" width="5" height="21" rx="2"/></g>',
        f'<path d="M11 15l8-3 8 3 8-4" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="35" cy="11" r="2" fill="{GOLD}"/>',
    ],
    "monitor": [
        f'<rect x="8" y="11" width="32" height="22" rx="4.5" fill="{G}"/>',
        f'<rect x="11" y="14" width="26" height="16" rx="2" fill="{DARK}"/>',
        f'<path d="M13 26l6-7 5 5 4-4 7 6" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<rect x="20" y="33" width="8" height="3.4" rx="1.4" fill="{GD}"/><rect x="15" y="36.4" width="18" height="3.2" rx="1.6" fill="{GD}"/>',
    ],
    "security": [
        f'<path d="M24 8l13 4.5v9.5c0 9-5.5 15.5-13 19.5-7.5-4-13-10.5-13-19.5v-9.5z" fill="{G}"/>',
        f'<path d="M24 8l13 4.5v9.5c0 9-5.5 15.5-13 19.5z" fill="#ffffff" opacity="0.12"/>',
        f'<path d="M18.5 23l4 4.5L30 19.5" fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "user": [
        f'<circle cx="24" cy="18" r="7.5" fill="{G}"/>',
        f'<path d="M10.5 38c1.5-8.5 7-13 13.5-13s12 4.5 13.5 13a2 2 0 0 1-2 2.4h-23A2 2 0 0 1 10.5 38z" fill="{G}"/>',
        f'<path d="M24 25c6.5 0 12 4.5 13.5 13a2 2 0 0 1-2 2.4H24z" fill="#ffffff" opacity="0.14"/>',
    ],
    "power": [
        f'<path d="M18.5 13a12 12 0 1 0 11 0" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<rect x="22.2" y="8" width="3.6" height="14" rx="1.8" fill="{GOLD}"/>',
    ],
    "update": [
        f'<path d="M35 17.5A12.5 12.5 0 1 0 36.5 24" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M36 12v6.5h-6.5" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="24" cy="24" r="3.4" fill="{WHITE}"/>',
    ],
    "installer": [
        f'<path d="M24 9v13" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M17.5 17l6.5 6.5L30.5 17" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M11 30v2a5 5 0 0 0 5 5h16a5 5 0 0 0 5-5v-2" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round"/>',
    ],
    "repair": [
        f'<path d="M30 11a7.5 7.5 0 0 0-8.6 10.2l-9.2 9.2a3.6 3.6 0 1 0 5.1 5.1l9.2-9.2A7.5 7.5 0 0 0 36.7 18l-4.6 4.6-3.7-1-1-3.7z" fill="{G}"/>',
        f'<path d="M30 11a7.5 7.5 0 0 0-8.6 10.2l2.5 2.5A7.5 7.5 0 0 0 36.7 18z" fill="#ffffff" opacity="0.16"/>',
    ],
    "restore": [
        f'<path d="M12.5 17.5A12.5 12.5 0 1 1 11.5 24" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M11 12v6.5h6.5" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M24 17.5V24l5 3.5" fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "reset": [
        f'<path d="M35 17.5A12.5 12.5 0 1 0 36.5 24" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M36 12v6.5h-6.5" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="24" cy="24" r="3.8" fill="{WHITE}"/>',
    ],
    "backup": [
        f'<path d="M13 32a8.5 8.5 0 0 1 1.2-16.9 10 10 0 0 1 19.3 1.7A8 8 0 0 1 33 32z" fill="{G}"/>',
        f'<path d="M24 24v8M20.5 28.5l3.5 3.5 3.5-3.5" fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "boot": [
        f'<circle cx="24" cy="24" r="9" fill="{G}"/>',
        f'<circle cx="24" cy="24" r="9" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.25"/>',
        f'<path d="M24 6v5M24 37v5M6 24h5M37 24h5M11 11l3.5 3.5M33.5 33.5L37 37M37 11l-3.5 3.5M14.5 33.5L11 37" stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round"/>',
    ],
    "accessibility": [
        f'<circle cx="24" cy="12" r="4" fill="{G}"/>',
        f'<path d="M9.5 18.5c9.5 3.2 19.5 3.2 29 0" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round"/>',
        f'<path d="M24 21v9l-6.5 11M24 30l6.5 11" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="24" cy="12" r="4" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.3"/>',
    ],
    "developer": [
        f'<path d="M16.5 16L7.5 24l9 8" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M31.5 16l9 8-9 8" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M27 12l-6 24" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>',
    ],
    "about": [
        f'<circle cx="24" cy="24" r="14.5" fill="{G}"/>',
        f'<path d="M24 21v10" stroke="{WHITE}" stroke-width="3.4" stroke-linecap="round"/>',
        f'<circle cx="24" cy="15.5" r="2.1" fill="{WHITE}"/>',
    ],
    # ── universal UI / launcher glyphs ─────────────────────────────────────
    "settings": [
        f'<path d="M24 8l2.2 3.1a11 11 0 0 1 3.1 1.1l3.4-.9 2.6 2.6-.9 3.4a11 11 0 0 1 1.1 3.1L38.6 23v2.4l-3.1 1.6a11 11 0 0 1-1.1 3.1l.9 3.4-2.6 2.6-3.4-.9a11 11 0 0 1-3.1 1.1L24 40l-2.2-3.1a11 11 0 0 1-3.1-1.1l-3.4.9-2.6-2.6.9-3.4a11 11 0 0 1-1.1-3.1L9.4 25.4v-2.4l3.1-1.6a11 11 0 0 1 1.1-3.1l-.9-3.4 2.6-2.6 3.4.9a11 11 0 0 1 3.1-1.1z" fill="{G}"/>',
        f'<circle cx="24" cy="24" r="6.5" fill="{INK}"/>',
        f'<circle cx="24" cy="24" r="6.5" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.25"/>',
    ],
    "search": [
        f'<circle cx="21" cy="21" r="11" fill="{G}"/>',
        f'<circle cx="21" cy="21" r="11" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.25"/>',
        f'<circle cx="17.5" cy="17.5" r="3.5" fill="#ffffff" opacity="0.3"/>',
        f'<path d="M30 30l8 8" stroke="{GOLD}" stroke-width="4.4" stroke-linecap="round"/>',
    ],
    "trash": [
        f'<path d="M12 15h24l-1.6 19a4 4 0 0 1-4 3.6H17.6a4 4 0 0 1-4-3.6z" fill="{G}"/>',
        f'<rect x="9.5" y="11.5" width="29" height="4" rx="2" fill="{GD}"/>',
        f'<path d="M20 9.5a4 4 0 0 1 8 0" fill="none" stroke="{GD}" stroke-width="2.6"/>',
        f'<path d="M19 20v11M24 20v11M29 20v11" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" opacity="0.5"/>',
    ],
    "edit": [
        f'<path d="M28 9l11 11-20 20H8V31z" fill="{G}"/>',
        f'<path d="M28 9l11 11 1.5-5.5a3.5 3.5 0 0 0-1-3L35.5 8a3.5 3.5 0 0 0-3-1z" fill="{GOLD}"/>',
        f'<path d="M28 9l11 11" stroke="{INK}" stroke-width="1.4" opacity="0.4"/>',
    ],
    "share": [
        f'<circle cx="33" cy="13" r="5" fill="{G}"/><circle cx="33" cy="35" r="5" fill="{G}"/>',
        f'<circle cx="14" cy="24" r="5" fill="{GOLD}"/>',
        f'<path d="M18.3 21.5l10.4-6M18.3 26.5l10.4 6" stroke="{WHITE}" stroke-width="2.4" opacity="0.85"/>',
    ],
    "copy": [
        f'<rect x="16" y="16" width="23" height="23" rx="5" fill="{G}"/>',
        f'<path d="M31 12V10a4 4 0 0 0-4-4H13a4 4 0 0 0-4 4v14a4 4 0 0 0 4 4h2" fill="none" stroke="{GD}" stroke-width="3"/>',
    ],
    "cut": [
        f'<circle cx="14" cy="14" r="5.5" fill="{G}"/><circle cx="14" cy="34" r="5.5" fill="{G}"/>',
        f'<path d="M18 16.5L38 33M18 31.5L38 15" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>',
    ],
    "paste": [
        f'<rect x="11" y="12" width="26" height="26" rx="5" fill="{G}"/>',
        f'<path d="M19 12a5 5 0 0 1 10 0" fill="none" stroke="{GD}" stroke-width="3"/>',
        f'<path d="M17 24h14M17 30h14" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" opacity="0.5"/>',
    ],
    "refresh": [
        f'<path d="M35 17.5A12.5 12.5 0 1 0 36.5 24" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M36 12v6.5h-6.5" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "back": [f'<path d="M29 11L15 24l14 13" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'],
    "forward": [f'<path d="M19 11l14 13-14 13" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'],
    "close": [f'<path d="M14 14l20 20M34 14L14 34" stroke="{G}" stroke-width="4" stroke-linecap="round"/>'],
    "menu": [f'<rect x="10" y="14" width="28" height="3.6" rx="1.8" fill="{G}"/><rect x="10" y="22" width="28" height="3.6" rx="1.8" fill="{G}"/><rect x="10" y="30" width="28" height="3.6" rx="1.8" fill="{G}"/>'],
    "more": [f'<circle cx="12" cy="24" r="3" fill="{G}"/><circle cx="24" cy="24" r="3" fill="{G}"/><circle cx="36" cy="24" r="3" fill="{G}"/>'],
    "download": [
        f'<path d="M24 9v16" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M16 19l8 8 8-8" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M10 33v1a5 5 0 0 0 5 5h18a5 5 0 0 0 5-5v-1" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round"/>',
    ],
    "upload": [
        f'<path d="M24 25V9" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M16 17l8-8 8 8" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M10 33v1a5 5 0 0 0 5 5h18a5 5 0 0 0 5-5v-1" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round"/>',
    ],
    "check": [f'<path d="M12 25l7 7 15-16" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'],
    "warning": [
        f'<path d="M24 9l17 29H7z" fill="{GOLD}" stroke="{GOLD}" stroke-width="2" stroke-linejoin="round"/>',
        f'<path d="M24 20v8" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><circle cx="24" cy="32" r="1.8" fill="{INK}"/>',
    ],
    "error": [
        f'<circle cx="24" cy="24" r="14.5" fill="{GOLD}"/>',
        f'<path d="M18.5 18.5l11 11M29.5 18.5l-11 11" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>',
    ],
    "lock": [
        f'<path d="M15 22h18v13a4 4 0 0 1-4 4H19a4 4 0 0 1-4-4z" fill="{G}"/>',
        f'<path d="M17 22v-4a7 7 0 0 1 14 0v4" fill="none" stroke="{GD}" stroke-width="3.4"/>',
        f'<circle cx="24" cy="28" r="2.4" fill="{GOLD}"/><path d="M24 29.5v3.5" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"/>',
    ],
    "wifi": [
        f'<path d="M9 20a20 20 0 0 1 30 0" fill="none" stroke="{G}" stroke-width="3.2" stroke-linecap="round"/>',
        f'<path d="M14 26a12 12 0 0 1 20 0" fill="none" stroke="{G}" stroke-width="3.2" stroke-linecap="round"/>',
        f'<path d="M19 32a5.5 5.5 0 0 1 10 0" fill="none" stroke="{G}" stroke-width="3.2" stroke-linecap="round"/>',
        f'<circle cx="24" cy="37" r="2.6" fill="{GOLD}"/>',
    ],
    "battery": [
        f'<rect x="8" y="16" width="28" height="16" rx="4" fill="none" stroke="{G}" stroke-width="2.8"/>',
        f'<rect x="37" y="21" width="3.5" height="6" rx="1.5" fill="{G}"/>',
        f'<rect x="11.5" y="19.5" width="16" height="9" rx="2" fill="{G}"/>',
    ],
    "bluetooth": [
        f'<path d="M24 9l7 6-14 12M24 9L17 15l7 6-7 6 7 6" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M24 39l7-6-14-12" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
    "volume": [
        f'<path d="M12 20h5l8-6v20l-8-6h-5z" fill="{G}"/>',
        f'<path d="M30 19a7 7 0 0 1 0 10M33.5 15.5a11 11 0 0 1 0 17" fill="none" stroke="{GOLD}" stroke-width="2.8" stroke-linecap="round"/>',
    ],
    "keyboard": [
        f'<rect x="8" y="14" width="32" height="20" rx="4" fill="{G}"/>',
        f'<g fill="{INK}" opacity="0.55"><rect x="12" y="18" width="3.4" height="3.4" rx="1"/><rect x="17.5" y="18" width="3.4" height="3.4" rx="1"/><rect x="23" y="18" width="3.4" height="3.4" rx="1"/><rect x="28.5" y="18" width="3.4" height="3.4" rx="1"/><rect x="12" y="24" width="24" height="3.6" rx="1.6"/></g>',
    ],
    "network": [
        f'<circle cx="24" cy="24" r="14" fill="{G}"/>',
        f'<path d="M10 24h28M24 10c-5 4-5 24 0 28M24 10c5 4 5 24 0 28" fill="none" stroke="{WHITE}" stroke-width="1.6" opacity="0.8"/>',
    ],
    "star": [
        f'<path d="M24 8l4.6 9.4L38.5 19l-7.4 7.2 1.8 10.3L24 31.8l-8.9 4.7 1.8-10.3L9.5 19l9.9-1.6z" fill="{GOLD}"/>',
        f'<path d="M24 8l4.6 9.4L38.5 19l-4.5.4-10-4.5z" fill="#ffffff" opacity="0.18"/>',
    ],
    "tag": [
        f'<path d="M28 9H15a4 4 0 0 0-4 4v13l14 14 14-14z" fill="{G}"/>',
        f'<circle cx="18" cy="16" r="2.6" fill="{WHITE}"/>',
    ],
    "cloud": [
        f'<path d="M15 34a7 7 0 0 1 .8-14 9 9 0 0 1 17.2 1.6A7.5 7.5 0 0 1 33 34z" fill="{G}"/>',
        f'<path d="M15 34a7 7 0 0 1 .8-14 9 9 0 0 1 17.2 1.6" fill="none" stroke="#ffffff" stroke-width="1.4" opacity="0.25"/>',
    ],
    "folder-add": [
        f'<path d="M9 15a4 4 0 0 1 4-4h7l4 4h11a4 4 0 0 1 4 4v13a4 4 0 0 1-4 4H13a4 4 0 0 1-4-4z" fill="{G}"/>',
        f'<path d="M24 21v8M20 25h8" stroke="{WHITE}" stroke-width="2.6" stroke-linecap="round"/>',
    ],
    "play": [f'<path d="M18 14l16 10-16 10z" fill="{G}"/>'],
    "pause": [f'<rect x="16" y="13" width="6" height="22" rx="2" fill="{G}"/><rect x="26" y="13" width="6" height="22" rx="2" fill="{G}"/>'],
    "stop": [f'<rect x="14" y="14" width="20" height="20" rx="3" fill="{GOLD}"/>'],
    "next": [f'<path d="M14 14l12 10-12 10z" fill="{G}"/><rect x="28" y="14" width="4.5" height="20" rx="2" fill="{G}"/>'],
    "prev": [f'<path d="M34 14L22 24l12 10z" fill="{G}"/><rect x="15.5" y="14" width="4.5" height="20" rx="2" fill="{G}"/>'],
    "rotate": [
        f'<path d="M35 17.5A12.5 12.5 0 1 0 36.5 24" fill="none" stroke="{G}" stroke-width="3.6" stroke-linecap="round"/>',
        f'<path d="M36 12v6.5h-6.5" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<circle cx="24" cy="24" r="3.4" fill="{WHITE}"/>',
    ],
    "crop": [
        f'<path d="M14 6v26a2 2 0 0 0 2 2h26" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round"/>',
        f'<path d="M34 42V16a2 2 0 0 0-2-2H6" fill="none" stroke="{GOLD}" stroke-width="3.4" stroke-linecap="round"/>',
    ],
    "filter": [f'<path d="M11 12h26l-9.5 11v9l-7 4v-13z" fill="{G}"/>'],
    "info": [f'<circle cx="24" cy="24" r="14.5" fill="{G}"/><path d="M24 21v10" stroke="{WHITE}" stroke-width="3.4" stroke-linecap="round"/><circle cx="24" cy="15.5" r="2.1" fill="{WHITE}"/>'],
    "chat": [
        f'<path d="M10 14a5 5 0 0 1 5-5h18a5 5 0 0 1 5 5v13a5 5 0 0 1-5 5H20l-8 6v-6a5 5 0 0 1-2-4z" fill="{G}"/>',
        f'<path d="M10 14a5 5 0 0 1 5-5h18a5 5 0 0 1 5 5v4H10z" fill="#ffffff" opacity="0.12"/>',
        f'<circle cx="18" cy="21" r="2.2" fill="{WHITE}"/><circle cx="24" cy="21" r="2.2" fill="{WHITE}"/><circle cx="30" cy="21" r="2.2" fill="{WHITE}"/>',
    ],
    "disk": [
        f'<rect x="9" y="12" width="30" height="24" rx="5" fill="{G}"/>',
        f'<rect x="12" y="15" width="24" height="18" rx="3" fill="{DARK}"/>',
        f'<circle cx="24" cy="24" r="6" fill="none" stroke="{G}" stroke-width="2.4"/>',
        f'<circle cx="24" cy="24" r="2" fill="{GOLD}"/>',
    ],
    "terminal-dbg": [
        f'<rect x="9" y="11" width="30" height="26" rx="6" fill="{DARK}"/>',
        f'<path d="M13.5 20l5 4.5-5 4.5" fill="none" stroke="{G}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<rect x="21.5" y="29" width="9" height="2.6" rx="1.3" fill="{GOLD}"/>',
    ],
}

# names that are "apps" (get the tile); pure UI glyphs get a transparent
# background so they can sit on any widget.
TILED = {
    "terminal", "files", "home", "browser", "mail", "music", "video", "photos",
    "text-editor", "pdf", "calculator", "calendar", "clock", "screenshot",
    "recorder", "task-manager", "monitor", "security", "user", "power", "update",
    "installer", "repair", "restore", "reset", "backup", "boot", "accessibility",
    "developer", "about", "settings", "search", "trash", "star", "tag", "cloud",
    "chat", "disk",
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
    "upload": "document-send", "check": "emblem-ok", "warning": "dialog-warning",
    "error": "dialog-error", "lock": "system-lock-screen", "wifi": "network-wireless",
    "battery": "battery-full", "bluetooth": "network-transmit", "volume": "audio-volume-high",
}


def svg(name, size=48):
    body = "\n".join(ICONS[name])
    tile = TILE if name in TILED else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{size}" height="{size}">\n{DEFS}\n{tile}\n{body}\n</svg>'


def main():
    apps = os.path.join(OUT, "apps", "scalable")
    actions = os.path.join(OUT, "actions", "scalable")
    for d in (apps, actions):
        os.makedirs(d, exist_ok=True)
    # wipe stale
    for d in (apps, actions):
        for f in os.listdir(d):
            if f.endswith(".svg"):
                os.remove(os.path.join(d, f))
    n_app = n_act = 0
    for name, _ in ICONS.items():
        target = apps if name in TILEd_set() else actions
        with open(os.path.join(target, f"{name}.svg"), "w") as f:
            f.write(svg(name))
        if name in TILEd_set():
            n_app += 1
        else:
            n_act += 1
    # index.theme
    with open(os.path.join(OUT, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=Simorgh\nInherits=Papirus-Dark,breeze,Adwaita\n"
                "Directories=" + ",".join(sorted({os.path.relpath(apps, OUT), os.path.relpath(actions, OUT)})) + "\n\n")
        for d in (apps, actions):
            rel = os.path.relpath(d, OUT)
            f.write(f"[{rel}]\nSize=48\nType=Scalable\nMinSize=16\nMaxSize=512\n\n")
    # freedesktop alias symlinks
    for name, std in INDEX_APPS.items():
        if name in ICONS:
            src = os.path.join(apps if name in TILEd_set() else actions, f"{name}.svg")
            dst = os.path.join(apps if name in TILEd_set() else actions, f"{std}.svg")
            if os.path.exists(src) and not os.path.lexists(dst):
                os.symlink(os.path.basename(src), dst)
    print(f"icons written: {n_app} tiled apps + {n_act} ui glyphs, {len(INDEX_APPS)} aliases")

    if "--sheet" in sys.argv:
        make_sheet(os.path.abspath(sys.argv[sys.argv.index("--sheet") + 1]))


def TILEd_set():
    return TILED


def make_sheet(path):
    import cairosvg
    names = [n for n in ICONS if n in TILEd_set()] + [n for n in ICONS if n not in TILEd_set()]
    cols = 8
    cell = 96
    pad = 12
    rows = (len(names) + cols - 1) // cols
    import io
    pngs = []
    for n in names:
        png = cairosvg.svg2png(bytestring=svg(n, 72).encode(), output_width=72, output_height=72)
        pngs.append(png)
    # compose with PIL if present, else just write first as sanity
    try:
        from PIL import Image
        sheet = Image.new("RGBA", (cols * (cell) + pad, rows * (cell) + pad), (13, 17, 28, 255))
        for i, png in enumerate(pngs):
            im = Image.open(io.BytesIO(png))
            x = pad + (i % cols) * cell + (cell - 72) // 2
            y = pad + (i // cols) * cell + (cell - 72) // 2
            sheet.paste(im, (x, y), im)
        sheet.save(path)
        print("sheet:", path)
    except Exception as e:
        print("PIL not available for sheet:", e)


if __name__ == "__main__":
    main()
