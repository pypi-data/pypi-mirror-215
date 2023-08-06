from tkadw import AdwDrawRoundEntry3


class GTkEntry(AdwDrawRoundEntry3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "entry_radius": 11,

                "entry_padding": (5, 5),

                "entry_frame_back": "#eaeaea",
                "entry_border_width": 1,
                "entry_bottom_width": 0,

                "entry_border": "#cdc7c2",
                "entry_back": "#ffffff",
                "entry_text_back": "#000000",
                "entry_bottom_line": "#eaeaea",

                "entry_focusin_border": "#3584e4",
                "entry_focusin_back": "#ffffff",
                "entry_focusin_text_back": "#000000",
                "entry_focusin_bottom_line": "#185fb4",
                "entry_focusin_bottom_width": 0,
            }
        )


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    entry = GTkEntry(text="GTkEntry")
    entry.pack(ipadx=5)

    root.mainloop()