# SimorghOS — shared GTK3 UI layer for core apps
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk  # noqa: E402

CSS_PATHS = ("/etc/simorgh/ui.css",)
ICON_THEME = "Simorgh"


def init(name: str, width=560, height=640):
    """Common bootstrap: icon theme, css, rtl awareness, window."""
    Gtk.init()
    screen = Gdk.Screen.get_default()
    for css in CSS_PATHS:
        if os.path.exists(css):
            prov = Gtk.CssProvider()
            prov.load_from_path(css)
            Gtk.StyleContext.add_provider_for_screen(
                screen, prov, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    st = Gtk.Settings.get_default()
    st.set_property("gtk-application-prefer-dark-theme", True)
    st.set_property("gtk-icon-theme-name", ICON_THEME)
    win = Gtk.Window(title=name)
    win.set_default_size(width, height)
    win.set_position(Gtk.WindowPosition.CENTER)
    win.connect("destroy", Gtk.main_quit)
    try:
        win.set_icon_name(name.split()[0].lower())
    except Exception:
        pass
    return win


def header(win, title, subtitle="", icon=None):
    hb = Gtk.HeaderBar(show_close_button=True)
    hb.set_title(title)
    if subtitle:
        hb.set_subtitle(subtitle)
    if icon:
        img = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.LARGE_TOOLBAR)
        hb.pack_start(img)
    win.set_titlebar(hb)
    return hb


def card():
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.set_margin_start(14)
    box.set_margin_end(14)
    box.set_margin_top(10)
    box.set_margin_bottom(10)
    box.get_style_context().add_class("simorgh-card")
    return box


def label(text, cls=None, size=None, bold=False):
    lb = Gtk.Label(label=text, xalign=0, wrap=True)
    if cls:
        lb.get_style_context().add_class(cls)
    if size:
        lb.override_font(_font(size, bold))
    elif bold:
        lb.override_font(_font(11, True))
    return lb


def _font(size, bold):
    import Pango
    d = Gtk.Settings.get_default().get_property("gtk-font-name").split()
    name = " ".join(d[:-1]) or "Vazirmatn"
    return Pango.FontDescription(f"{name} {'Bold ' if bold else ''}{size}")


def run_cmd(argv, done=None):
    """Run subprocess in thread; call done(ok, output) on GTK main loop."""
    import subprocess
    import threading

    def work():
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=600)
            ok, out = r.returncode == 0, (r.stdout or "") + (r.stderr or "")
        except Exception as e:  # noqa: BLE001
            ok, out = False, str(e)
        if done:
            from gi.repository import GLib
            GLib.idle_add(done, ok, out)

    threading.Thread(target=work, daemon=True).start()


def pkexec(argv, done=None):
    run_cmd(["pkexec", "sh", "-c", " ".join(argv)], done)
