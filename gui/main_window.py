import os
import tkinter as tk


try:
    import customtkinter as ctk
except Exception:
    ctk = None


CUSTOMTK_AVAILABLE = ctk is not None
USE_CUSTOMTK = CUSTOMTK_AVAILABLE and os.environ.get("ELDEN_MANAGER_CUSTOMTK", "").lower() in {
    "1",
    "true",
    "yes",
}

# The legacy UI still creates Tk widgets directly. Keep dialogs on tk.Toplevel
# until each window is migrated to CTk widgets, otherwise mixed parents can fail.
ToplevelBase = tk.Toplevel
PALETTE = {
    "bg": "#151515",
    "card": "#1f1d1a",
    "card_alt": "#26231f",
    "line": "#514638",
    "text": "#f1e7d2",
    "muted": "#b9ad99",
    "accent": "#c8924f",
    "accent_dark": "#8f6f3f",
    "danger": "#9d4f43",
    "entry": "#121110",
}


def _apply_legacy_dark_theme(root):
    dark_bg = PALETTE["bg"]
    panel_bg = PALETTE["entry"]
    text_fg = PALETTE["text"]
    muted_fg = PALETTE["muted"]

    root.configure(bg=dark_bg)
    root.option_add("*Background", dark_bg)
    root.option_add("*Foreground", text_fg)
    root.option_add("*activeBackground", "#2d2a25")
    root.option_add("*activeForeground", "#f4ead8")
    root.option_add("*Entry.Background", panel_bg)
    root.option_add("*Entry.Foreground", text_fg)
    root.option_add("*Entry.InsertBackground", text_fg)
    root.option_add("*Listbox.Background", panel_bg)
    root.option_add("*Listbox.Foreground", text_fg)
    root.option_add("*Listbox.selectBackground", "#8f6f3f")
    root.option_add("*Listbox.selectForeground", "#fff6e8")
    root.option_add("*Button.Background", "#2b2925")
    root.option_add("*Button.Foreground", muted_fg)


def card(parent, **kwargs):
    options = {
        "bg": PALETTE["card"],
        "highlightthickness": 1,
        "highlightbackground": PALETTE["line"],
        "highlightcolor": PALETTE["accent"],
        "bd": 0,
    }
    options.update(kwargs)
    return tk.Frame(parent, **options)


def label(parent, text, role="body", **kwargs):
    fonts = {
        "title": ("Georgia", 25, "bold"),
        "subtitle": ("Segoe UI", 10),
        "section": ("Segoe UI", 12, "bold"),
        "body": ("Segoe UI", 10),
        "small": ("Segoe UI", 9),
    }
    colors = {
        "title": PALETTE["text"],
        "subtitle": PALETTE["muted"],
        "section": PALETTE["accent"],
        "body": PALETTE["text"],
        "small": PALETTE["muted"],
    }
    options = {
        "text": text,
        "bg": kwargs.pop("bg", PALETTE["card"]),
        "fg": kwargs.pop("fg", colors.get(role, PALETTE["text"])),
        "font": kwargs.pop("font", fonts.get(role, fonts["body"])),
        "justify": kwargs.pop("justify", "left"),
        "anchor": kwargs.pop("anchor", "w"),
    }
    options.update(kwargs)
    return tk.Label(parent, **options)


def button(parent, text, command=None, variant="normal", **kwargs):
    backgrounds = {
        "normal": PALETTE["card_alt"],
        "primary": PALETTE["accent_dark"],
        "danger": PALETTE["danger"],
    }
    options = {
        "text": text,
        "command": command,
        "bg": backgrounds.get(variant, PALETTE["card_alt"]),
        "fg": PALETTE["text"],
        "activebackground": PALETTE["accent"],
        "activeforeground": "#17120d",
        "font": ("Segoe UI", 10, "bold"),
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2",
        "padx": 14,
        "pady": 8,
    }
    options.update(kwargs)
    return tk.Button(parent, **options)


def entry(parent, **kwargs):
    options = {
        "bg": PALETTE["entry"],
        "fg": PALETTE["text"],
        "insertbackground": PALETTE["text"],
        "highlightthickness": 1,
        "highlightbackground": PALETTE["line"],
        "highlightcolor": PALETTE["accent"],
        "bd": 0,
        "font": ("Segoe UI", 10),
    }
    options.update(kwargs)
    return tk.Entry(parent, **options)


def listbox(parent, **kwargs):
    options = {
        "bg": PALETTE["entry"],
        "fg": PALETTE["text"],
        "selectbackground": PALETTE["accent_dark"],
        "selectforeground": "#fff6e8",
        "highlightthickness": 1,
        "highlightbackground": PALETTE["line"],
        "highlightcolor": PALETTE["accent"],
        "bd": 0,
        "activestyle": "none",
        "font": ("Segoe UI", 10, "bold"),
    }
    options.update(kwargs)
    return tk.Listbox(parent, **options)


def create_root(title, geometry="830x561", resizable=(False, False)):
    if USE_CUSTOMTK:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root = ctk.CTk()
    else:
        root = tk.Tk()
        _apply_legacy_dark_theme(root)

    root.title(title)
    root.geometry(geometry)
    root.resizable(width=resizable[0], height=resizable[1])
    return root
