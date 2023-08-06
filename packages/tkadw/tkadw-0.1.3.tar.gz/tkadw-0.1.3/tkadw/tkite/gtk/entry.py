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

                "entry_border": "#cdc7c2",
                "entry_back": "#ffffff",
                "entry_text_back": "#000000",
                "entry_bottom_line": "#eaeaea",
                "entry_bottom_width": 0,

                "entry_focusin_border": "#3584e4",
                "entry_focusin_back": "#ffffff",
                "entry_focusin_text_back": "#000000",
                "entry_focusin_bottom_line": "#185fb4",
                "entry_focusin_bottom_width": 0,
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "entry_radius": 11,

                "entry_padding": (5, 5),

                "entry_frame_back": "#eaeaea",
                "entry_border_width": 1,

                "entry_border": "#1f1f1f",
                "entry_back": "#2d2d2d",
                "entry_text_back": "#cccccc",
                "entry_bottom_line": "#eaeaea",
                "entry_bottom_width": 0,

                "entry_focusin_border": "#3584e4",
                "entry_focusin_back": "#2d2d2d",
                "entry_focusin_text_back": "#ffffff",
                "entry_focusin_bottom_line": "#3584e4",
                "entry_focusin_bottom_width": 0,
            }
        )


class GTkDarkEntry(GTkEntry):
    def default_palette(self):
        self.palette_gtk_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.configure(background="#1e1e1e")

    entry = GTkDarkEntry(text="GTkEntry")
    entry.pack(fill="x", ipadx=5, padx=5, pady=5)

    entry2 = GTkDarkEntry(text="GTkDarkEntry")
    entry2.pack(fill="x", ipadx=5, padx=5, pady=5)

    root.mainloop()