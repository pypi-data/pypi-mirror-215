from tkinter.font import Font, nametofont
from tkadw.canvas.drawengine import AdwDrawEngine


# Entry
class AdwDrawBasicEntry(AdwDrawEngine):
    def __init__(self, *args, width=120, height=40, text: str = "", **kwargs):

        super().__init__(*args, width=width, height=height, highlightthickness=0, **kwargs)

        from tkinter import StringVar, Entry

        self.var = StringVar()
        self.var.set(text)

        self.entry = Entry(self, bd=0, textvariable=self.var)

        self._other()

        self.default_palette()

        self.text = text

        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_text_back = self.entry_text_back
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self.entry_text_font = nametofont("TkDefaultFont")

        self.bind("<Configure>", self._draw, add="+")
        self.bind("<Button>", self._click, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")
        self.bind("<FocusIn>", self._focus, add="+")
        self.entry.bind("<FocusIn>", self._focus, add="+")
        self.bind("<FocusOut>", self._focusout, add="+")
        self.entry.bind("<FocusOut>", self._focusout, add="+")

        self._draw(None)

    def set(self, text: str):
        self.var.set(text)

    def get(self):
        return self.var.get()

    def _other(self):
        if hasattr(self, "button_frame_back"):
            self.configure(background=self.button_frame_back, borderwidth=0)

    def _draw(self, evt):
        self.delete("all")

        self.entry_frame = self.create_rectangle(
            0, 0, self.winfo_width() - 1, self.winfo_height() - 1,
            width=self.entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.entry_border_width - 5 - self.entry_padding[0],
            height=self.winfo_height() - self.entry_border_width - 5 - self.entry_padding[1],
            window=self.entry
        )

        self.entry_bottom = self.create_rectangle(1, self.winfo_height() - self._entry_bottom_width - 1,
                                                  self.winfo_width() - 1, self.winfo_height() - 1,
                                                  fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                  width=0)

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back, insertbackground=self._entry_text_back)

    def _focus(self, evt=None):
        self._entry_back = self.entry_focusin_back
        self._entry_border = self.entry_focusin_border
        self._entry_text_back = self.entry_focusin_text_back
        self._entry_bottom_line = self.entry_focusin_bottom_line
        self._entry_bottom_width = self.entry_focusin_bottom_width

        self._draw(None)

    def _focusout(self, evt=None):
        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_text_back = self.entry_text_back
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self._draw(None)

    def _click(self, evt=None):
        self.focus_set()

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        if not self.focus_get():
            self.hover = False
            self._entry_back = self.entry_back
            self._entry_border = self.entry_border
            self._entry_text_back = self.entry_text_back
            self._entry_bottom_line = self.entry_bottom_line
            self._entry_bottom_width = self.entry_bottom_width

            self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.entry_text_font
        else:
            self.entry_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "entry_padding": (3, 4),

                "entry_frame_back": "#f3f3f3",
                "entry_border_width": 1,
                "entry_bottom_width": 0,

                "entry_border": "#eaeaea",
                "entry_back": "#fdfdfd",
                "entry_text_back": "#5f5f5f",
                "entry_bottom_line": "#eaeaea",

                "entry_focusin_border": "#e2e2e2",
                "entry_focusin_back": "#f9f9f9",
                "entry_focusin_text_back": "#1a1a1a",
                "entry_focusin_bottom_line": "#185fb4",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "entry_padding": (3, 4),

                "entry_frame_back": "#202020",
                "entry_border_width": 1,

                "entry_border": "#454545",
                "entry_back": "#353535",
                "entry_text_back": "#cecece",
                "entry_bottom_line": "#ffffff",
                "entry_bottom_width": 0,

                "entry_focusin_border": "#454545",
                "entry_focusin_back": "#2f2f2f",
                "entry_focusin_text_back": "#ffffff",
                "entry_focusin_bottom_line": "#4cc2ff",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.entry_padding = dict["entry_padding"]

            self.entry_frame_back = dict["entry_frame_back"]
            self.entry_border_width = dict["entry_border_width"]

            self.entry_border = dict["entry_border"]
            self.entry_back = dict["entry_back"]
            self.entry_text_back = dict["entry_text_back"]
            self.entry_bottom_line = dict["entry_bottom_line"]
            self.entry_bottom_width = dict["entry_bottom_width"]

            self.entry_focusin_border = dict["entry_focusin_border"]
            self.entry_focusin_back = dict["entry_focusin_back"]
            self.entry_focusin_text_back = dict["entry_focusin_text_back"]
            self.entry_focusin_bottom_line = dict["entry_focusin_bottom_line"]
            self.entry_focusin_bottom_width = dict["entry_focusin_bottom_width"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "entry_padding": self.entry_padding,

                "entry_frame_back": self.entry_frame_back,
                "entry_border_width": self.entry_border_width,
                "entry_bottom_width": self.entry_bottom_width,

                "entry_border": self.entry_border,
                "entry_back": self.entry_back,
                "entry_text_back": self.entry_text_back,

                "entry_focusin_border": self.entry_focusin_border,
                "entry_focusin_back": self.entry_focusin_back,
                "entry_focusin_text_back": self.entry_focusin_text_back,
            }


class AdwDrawEntry(AdwDrawBasicEntry):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkEntry(AdwDrawBasicEntry):
    def default_palette(self):
        self.palette_dark()


# Rounded Entry
class AdwDrawBasicRoundEntry(AdwDrawBasicEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _other(self):
        if hasattr(self, "button_frame_back"):
            self.configure(background=self.button_frame_back, borderwidth=0)

    def border_radius(self, radius: float | int = None):
        if radius is None:
            return self.button_radius
        else:
            self.button_radius = radius

    def _draw(self, evt):
        self.delete("all")

        self.entry_frame = self.create_round_rect2(
            2, 2, self.winfo_width() - 3, self.winfo_height() - 3, self.entry_radius,
            width=self.entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.entry_border_width - 5 - self.entry_padding[0],
            height=self.winfo_height() - self.entry_border_width - 5 - self.entry_padding[1],
            window=self.entry
        )

        self.entry_bottom = self.create_rectangle(3 + self.entry_radius / 2,
                                                  self.winfo_height() - self._entry_bottom_width - 3,
                                                  self.winfo_width() - 3 - self.entry_radius / 2,
                                                  self.winfo_height() - 3.5,
                                                  fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                  width=0)

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back, insertbackground=self._entry_text_back)

    def _focus(self, evt=None):
        self._entry_back = self.entry_focusin_back
        self._entry_border = self.entry_focusin_border
        self._entry_text_back = self.entry_focusin_text_back
        self._entry_bottom_line = self.entry_focusin_bottom_line
        self._entry_bottom_width = self.entry_focusin_bottom_width

        self._draw(None)

    def _focusout(self, evt=None):
        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_text_back = self.entry_text_back
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self._draw(None)

    def _click(self, evt=None):
        self.focus_set()

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        if not self.focus_get():
            self.hover = False
            self._entry_back = self.entry_back
            self._entry_border = self.entry_border
            self._entry_text_back = self.entry_text_back
            self._entry_bottom_line = self.entry_bottom_line
            self._entry_bottom_width = self.entry_bottom_width

            self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.entry_text_font
        else:
            self.entry_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "entry_radius": 6,

                "entry_padding": (3, 4),

                "entry_frame_back": "#f3f3f3",
                "entry_border_width": 1,
                "entry_bottom_width": 0,

                "entry_border": "#eaeaea",
                "entry_back": "#fdfdfd",
                "entry_text_back": "#5f5f5f",
                "entry_bottom_line": "#eaeaea",

                "entry_focusin_border": "#e2e2e2",
                "entry_focusin_back": "#f9f9f9",
                "entry_focusin_text_back": "#1a1a1a",
                "entry_focusin_bottom_line": "#185fb4",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "entry_radius": 6,

                "entry_padding": (3, 4),

                "entry_frame_back": "#202020",
                "entry_border_width": 1,

                "entry_border": "#454545",
                "entry_back": "#353535",
                "entry_text_back": "#cecece",
                "entry_bottom_line": "#ffffff",
                "entry_bottom_width": 0,

                "entry_focusin_border": "#454545",
                "entry_focusin_back": "#2f2f2f",
                "entry_focusin_text_back": "#ffffff",
                "entry_focusin_bottom_line": "#4cc2ff",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.entry_radius = dict["entry_radius"]

            self.entry_padding = dict["entry_padding"]

            self.entry_frame_back = dict["entry_frame_back"]
            self.entry_border_width = dict["entry_border_width"]

            self.entry_border = dict["entry_border"]
            self.entry_back = dict["entry_back"]
            self.entry_text_back = dict["entry_text_back"]
            self.entry_bottom_line = dict["entry_bottom_line"]
            self.entry_bottom_width = dict["entry_bottom_width"]

            self.entry_focusin_border = dict["entry_focusin_border"]
            self.entry_focusin_back = dict["entry_focusin_back"]
            self.entry_focusin_text_back = dict["entry_focusin_text_back"]
            self.entry_focusin_bottom_line = dict["entry_focusin_bottom_line"]
            self.entry_focusin_bottom_width = dict["entry_focusin_bottom_width"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "entry_padding": self.entry_padding,

                "entry_frame_back": self.entry_frame_back,
                "entry_border_width": self.entry_border_width,
                "entry_bottom_width": self.entry_bottom_width,

                "entry_border": self.entry_border,
                "entry_back": self.entry_back,
                "entry_text_back": self.entry_text_back,

                "entry_focusin_border": self.entry_focusin_border,
                "entry_focusin_back": self.entry_focusin_back,
                "entry_focusin_text_back": self.entry_focusin_text_back,
            }


class AdwDrawRoundEntry(AdwDrawBasicRoundEntry):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkEntry(AdwDrawBasicRoundEntry):
    def default_palette(self):
        self.palette_dark()


class AdwDrawBasicRoundEntry3(AdwDrawBasicEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _other(self):
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def border_radius(self, radius: float | int = None):
        if radius is None:
            return self.button_radius
        else:
            self.button_radius = radius

    def _draw(self, evt):
        self.delete("all")

        self.create_round_rect4(
            0,
            0,
            self.winfo_width() - 1,
            self.winfo_height() - 1,
            self.entry_radius,
            width=self.entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        self.entry_frame = "button_frame"

        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.entry_border_width - self.entry_padding[0] - 2,
            height=self.winfo_height() - self.entry_border_width - self.entry_padding[1] - 2,
            window=self.entry
        )

        self.entry_bottom = self.create_rectangle(1 + self.entry_radius / 5,
                                                  self.winfo_height() - self._entry_bottom_width - 1,
                                                  self.winfo_width() - 1 - self.entry_radius / 5,
                                                  self.winfo_height() - 1,
                                                  fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                  width=0)

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back, insertbackground=self._entry_text_back)

    def _focus(self, evt=None):
        self._entry_back = self.entry_focusin_back
        self._entry_border = self.entry_focusin_border
        self._entry_text_back = self.entry_focusin_text_back
        self._entry_bottom_line = self.entry_focusin_bottom_line
        self._entry_bottom_width = self.entry_focusin_bottom_width

        self._draw(None)

    def _focusout(self, evt=None):
        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_text_back = self.entry_text_back
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self._draw(None)

    def _click(self, evt=None):
        self.focus_set()

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        if not self.focus_get():
            self.hover = False
            self._entry_back = self.entry_back
            self._entry_border = self.entry_border
            self._entry_text_back = self.entry_text_back
            self._entry_bottom_line = self.entry_bottom_line
            self._entry_bottom_width = self.entry_bottom_width

            self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.entry_text_font
        else:
            self.entry_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "entry_radius": 13,

                "entry_padding": (6, 4),

                "entry_frame_back": "#f3f3f3",
                "entry_border_width": 1,
                "entry_bottom_width": 0,

                "entry_border": "#eaeaea",
                "entry_back": "#fdfdfd",
                "entry_text_back": "#5f5f5f",
                "entry_bottom_line": "#eaeaea",

                "entry_focusin_border": "#e2e2e2",
                "entry_focusin_back": "#f9f9f9",
                "entry_focusin_text_back": "#1a1a1a",
                "entry_focusin_bottom_line": "#185fb4",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "entry_radius": 13,

                "entry_padding": (3, 4),

                "entry_frame_back": "#202020",
                "entry_border_width": 1,

                "entry_border": "#454545",
                "entry_back": "#353535",
                "entry_text_back": "#cecece",
                "entry_bottom_line": "#ffffff",
                "entry_bottom_width": 0,

                "entry_focusin_border": "#454545",
                "entry_focusin_back": "#2f2f2f",
                "entry_focusin_text_back": "#ffffff",
                "entry_focusin_bottom_line": "#4cc2ff",
                "entry_focusin_bottom_width": 2,
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.entry_radius = dict["entry_radius"]

            self.entry_padding = dict["entry_padding"]

            self.entry_frame_back = dict["entry_frame_back"]
            self.entry_border_width = dict["entry_border_width"]

            self.entry_border = dict["entry_border"]
            self.entry_back = dict["entry_back"]
            self.entry_text_back = dict["entry_text_back"]
            self.entry_bottom_line = dict["entry_bottom_line"]
            self.entry_bottom_width = dict["entry_bottom_width"]

            self.entry_focusin_border = dict["entry_focusin_border"]
            self.entry_focusin_back = dict["entry_focusin_back"]
            self.entry_focusin_text_back = dict["entry_focusin_text_back"]
            self.entry_focusin_bottom_line = dict["entry_focusin_bottom_line"]
            self.entry_focusin_bottom_width = dict["entry_focusin_bottom_width"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "entry_padding": self.entry_padding,

                "entry_frame_back": self.entry_frame_back,
                "entry_border_width": self.entry_border_width,
                "entry_bottom_width": self.entry_bottom_width,

                "entry_border": self.entry_border,
                "entry_back": self.entry_back,
                "entry_text_back": self.entry_text_back,

                "entry_focusin_border": self.entry_focusin_border,
                "entry_focusin_back": self.entry_focusin_back,
                "entry_focusin_text_back": self.entry_focusin_text_back,
            }


class AdwDrawRoundEntry3(AdwDrawBasicRoundEntry3):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkEntry3(AdwDrawBasicRoundEntry3):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    entry1 = AdwDrawEntry(text="Hello")
    entry1.pack(fill="x", padx=5, pady=5)

    entry2 = AdwDrawDarkEntry(text="Hello")
    entry2.pack(fill="x", padx=5, pady=5)

    entry3 = AdwDrawRoundEntry(text="Hello")
    entry3.pack(fill="x", padx=5, pady=5)

    entry4 = AdwDrawRoundDarkEntry(text="Hello")
    entry4.pack(fill="x", padx=5, pady=5)

    entry5 = AdwDrawRoundEntry3(text="Hello")
    entry5.pack(fill="x", padx=5, pady=5)

    entry6 = AdwDrawRoundDarkEntry3(text="Hello")
    entry6.pack(fill="x", padx=5, pady=5)

    root.mainloop()
