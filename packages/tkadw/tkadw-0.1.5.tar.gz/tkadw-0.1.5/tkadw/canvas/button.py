from tkinter.font import Font, nametofont
from tkadw.canvas.drawengine import AdwDrawEngine


# Button
class AdwDrawBasicButton(AdwDrawEngine):
    def __init__(self, *args, width=120, height=40, text: str = "", command=None, **kwargs):
        super().__init__(*args, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self._other()

        self.default_palette()

        self.text = text

        self._button_back = self.button_back
        self._button_border = self.button_border
        self._button_text_back = self.button_text_back

        self.button_text_font = nametofont("TkDefaultFont")

        self.bind("<Configure>", self._draw, add="+")
        self.bind("<Button>", self._click, add="+")
        self.bind("<ButtonRelease>", self._unclick, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")

        if command is not None:
            self.bind("<<Click>>", lambda event: command())

        self._draw(None)

    def configure(self, **kwargs):
        if "command" in kwargs:
            self.command = kwargs.pop("command")
            self.bind("<<Click>>", lambda event: self.command())
        elif "text" in kwargs:
            self.text = kwargs.pop("text")
            self._draw(None)
        else:
            super().configure(**kwargs)

    def _other(self):
        if hasattr(self, "button_frame_back"):
            self.configure(background=self.button_frame_back, borderwidth=0)

    def _draw(self, evt):
        self.delete("all")

        self.button_frame = self.create_rectangle(
            1.5, 1.5, self.winfo_width() - 3, self.winfo_height() - 3,
            width=self.button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def _click(self, evt=None):
        self.hover = True
        self._button_back = self.button_pressed_back
        self._button_border = self.button_pressed_border
        self._button_text_back = self.button_pressed_text_back

        self.focus_set()

        self._draw(None)

    def _unclick(self, evt=None):
        if self.hover:
            self._button_back = self.button_active_back
            self._button_border = self.button_active_border
            self._button_text_back = self.button_active_text_back

            self._draw(None)

            self.event_generate("<<Click>>")

    def _hover(self, evt=None):
        self.hover = True
        self._button_back = self.button_active_back
        self._button_border = self.button_active_border
        self._button_text_back = self.button_active_text_back

        self._draw(None)

    def _hover_release(self, evt=None):
        self.hover = False
        self._button_back = self.button_back
        self._button_border = self.button_border
        self._button_text_back = self.button_text_back

        self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.button_text_font
        else:
            self.button_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "button_frame_back": "#f3f3f3",

                "button_border_width": 1,

                "button_border": "#eaeaea",
                "button_back": "#fdfdfd",
                "button_text_back": "#1a1a1a",

                "button_active_border": "#e2e2e2",
                "button_active_back": "#f9f9f9",
                "button_active_text_back": "#5f5f5f",

                "button_pressed_border": "#e2e2e2",
                "button_pressed_back": "#f9f9f9",
                "button_pressed_text_back": "#8a8a8a",
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "button_frame_back": "#202020",

                "button_border_width": 1,

                "button_border": "#454545",
                "button_back": "#353535",
                "button_text_back": "#ffffff",

                "button_active_border": "#454545",
                "button_active_back": "#3a3a3a",
                "button_active_text_back": "#cecece",

                "button_pressed_border": "#454545",
                "button_pressed_back": "#2f2f2f",
                "button_pressed_text_back": "#9a9a9a",
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.button_frame_back = dict["button_frame_back"]
            self.button_border_width = dict["button_border_width"]

            self.button_border = dict["button_border"]
            self.button_back = dict["button_back"]
            self.button_text_back = dict["button_text_back"]

            self.button_active_border = dict["button_active_border"]
            self.button_active_back = dict["button_active_back"]
            self.button_active_text_back = dict["button_active_text_back"]

            self.button_pressed_border = dict["button_pressed_border"]
            self.button_pressed_back = dict["button_pressed_back"]
            self.button_pressed_text_back = dict["button_pressed_text_back"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "button_frame_back": self.button_frame_back,
                "button_border_width": self.button_border_width,

                "button_border": self.button_border,
                "button_back": self.button_back,
                "button_text_back": self.button_text_back,

                "button_active_border": self.button_active_border,
                "button_active_back": self.button_active_back,
                "button_active_text_back": self.button_active_text_back,

                "button_pressed_border": self.button_pressed_border,
                "button_pressed_back": self.button_pressed_back,
                "button_pressed_text_back": self.button_pressed_text_back,
            }


class AdwDrawButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette_dark()


class AdwDrawAccentButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette(
            {
                "button_frame_back": "#0067c0",

                "button_border_width": 1,

                "button_border": "#1473c5",
                "button_back": "#0067c0",
                "button_text_back": "#ffffff",

                "button_active_border": "#1473c5",
                "button_active_back": "#1975c5",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#3284cb",
                "button_pressed_back": "#3284cb",
                "button_pressed_text_back": "#fdfdfd",
            }
        )


# Round Button
class AdwDrawBasicRoundButton(AdwDrawBasicButton):
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

        self.button_frame = self.create_round_rect2(
            2, 2, self.winfo_width()-3, self.winfo_height()-3, self.button_radius,
            width=self.button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "button_radius": 8,

                "button_border_width": 1,

                "button_border": "#eaeaea",
                "button_back": "#fdfdfd",
                "button_text_back": "#1a1a1a",

                "button_active_border": "#e2e2e2",
                "button_active_back": "#f9f9f9",
                "button_active_text_back": "#5f5f5f",

                "button_pressed_border": "#e2e2e2",
                "button_pressed_back": "#f9f9f9",
                "button_pressed_text_back": "#8a8a8a",
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "button_radius": 8,

                "button_border_width": 1,

                "button_border": "#454545",
                "button_back": "#353535",
                "button_text_back": "#ffffff",

                "button_active_border": "#454545",
                "button_active_back": "#3a3a3a",
                "button_active_text_back": "#cecece",

                "button_pressed_border": "#454545",
                "button_pressed_back": "#2f2f2f",
                "button_pressed_text_back": "#9a9a9a",
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.button_radius = dict["button_radius"]

            self.button_border_width = dict["button_border_width"]

            self.button_border = dict["button_border"]
            self.button_back = dict["button_back"]
            self.button_text_back = dict["button_text_back"]

            self.button_active_border = dict["button_active_border"]
            self.button_active_back = dict["button_active_back"]
            self.button_active_text_back = dict["button_active_text_back"]

            self.button_pressed_border = dict["button_pressed_border"]
            self.button_pressed_back = dict["button_pressed_back"]
            self.button_pressed_text_back = dict["button_pressed_text_back"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "button_frame_back": self.button_frame_back,

                "button_border_width": self.button_border_width,

                "button_border": self.button_border,
                "button_back": self.button_back,
                "button_text_back": self.button_text_back,

                "button_active_border": self.button_active_border,
                "button_active_back": self.button_active_back,
                "button_active_text_back": self.button_active_text_back,

                "button_pressed_border": self.button_pressed_border,
                "button_pressed_back": self.button_pressed_back,
                "button_pressed_text_back": self.button_pressed_text_back,
            }


class AdwDrawRoundButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette(
            {
                "button_radius": 8,

                "button_border_width": 1,

                "button_border": "#1473c5",
                "button_back": "#0067c0",
                "button_text_back": "#ffffff",

                "button_active_border": "#1473c5",
                "button_active_back": "#1975c5",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#3284cb",
                "button_pressed_back": "#3284cb",
                "button_pressed_text_back": "#fdfdfd",
            }
        )


class AdwDrawRoundDarkButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette_dark()


class AdwDrawRoundButton2(AdwDrawBasicRoundButton):
    def _draw(self, evt):
        self.delete("all")

        self.create_round_rect3(
            "button_frame",
            2, 2, self.winfo_width()-3, self.winfo_height()-3, self.button_radius,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_frame = "button_frame"

        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton2(AdwDrawRoundButton2):
    def default_palette(self):
        self.palette(
            {
                "button_radius": 8,

                "button_border_width": 1,

                "button_border": "#1473c5",
                "button_back": "#0067c0",
                "button_text_back": "#ffffff",

                "button_active_border": "#1473c5",
                "button_active_back": "#1975c5",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#3284cb",
                "button_pressed_back": "#3284cb",
                "button_pressed_text_back": "#fdfdfd",
            }
        )


class AdwDrawRoundDarkButton2(AdwDrawRoundButton2):
    def default_palette(self):
        self.palette_dark()


class AdwDrawRoundButton3(AdwDrawBasicRoundButton):
    def _draw(self, evt):
        self.delete("all")

        self.create_round_rect4(
            self.button_border_width + 1, self.button_border_width + 1, self.winfo_width() - self.button_border_width -2, self.winfo_height() - self.button_border_width -2, self.button_radius,
            width=self.button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_frame = "button_frame"

        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton3(AdwDrawRoundButton3):
    def default_palette(self):
        self.palette(
            {
                "button_radius": 8,

                "button_border_width": 1,

                "button_border": "#1473c5",
                "button_back": "#0067c0",
                "button_text_back": "#ffffff",

                "button_active_border": "#1473c5",
                "button_active_back": "#1975c5",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#3284cb",
                "button_pressed_back": "#3284cb",
                "button_pressed_text_back": "#fdfdfd",
            }
        )


class AdwDrawRoundDarkButton3(AdwDrawRoundButton3):
    def default_palette(self):
        self.palette_dark()


# Circular Button
class AdwDrawBasicCircularButton(AdwDrawBasicButton):
    def __init__(self, *args, width=120, height=120, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _draw(self, evt):
        self.delete("all")

        self.button_frame = self.create_oval(
            1.5, 1.5, self.winfo_width() - 3, self.winfo_height() - 3,
            width=self.button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )


class AdwDrawCircularButton(AdwDrawBasicCircularButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawCircularDarkButton(AdwDrawBasicCircularButton):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    button = AdwDrawButton(text="Hello")
    button.bind("<<Click>>", lambda evt: print("button clicked"))
    button.pack(fill="x", padx=5, pady=5)

    button4 = AdwDrawRoundButton(text="Hello")
    button4.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button4.pack(fill="x", padx=5, pady=5)

    button7 = AdwDrawRoundButton2(text="Hello")
    button7.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button7.pack(fill="x", padx=5, pady=5)

    button10 = AdwDrawRoundButton3(text="Hello")
    button10.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button10.pack(fill="x", padx=5, pady=5)

    button13 = AdwDrawCircularButton(text="Hello")
    button13.bind("<<Click>>", lambda evt: print("button6 clicked"))
    button13.pack(fill="x", padx=5, pady=5)

    root.mainloop()
