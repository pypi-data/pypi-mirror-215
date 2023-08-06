from tkadw import AdwDrawText


class GTkTextBox(AdwDrawText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "text_padding": (3, 3),

                "text_frame_back": "#eaeaea",
                "text_border_width": 1,

                "text_border": "#cdc7c2",
                "text_back": "#ffffff",
                "text_text_back": "#000000",
                "text_bottom_line": "#eaeaea",
                "text_bottom_width": 0,

                "text_focusin_border": "#3584e4",
                "text_focusin_back": "#ffffff",
                "text_focusin_text_back": "#000000",
                "text_focusin_bottom_line": "#185fb4",
                "text_focusin_bottom_width": 0,
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "text_padding": (3, 3),

                "text_frame_back": "#eaeaea",
                "text_border_width": 1,

                "text_border": "#1f1f1f",
                "text_back": "#2d2d2d",
                "text_text_back": "#cccccc",
                "text_bottom_line": "#eaeaea",
                "text_bottom_width": 0,

                "text_focusin_border": "#3584e4",
                "text_focusin_back": "#2d2d2d",
                "text_focusin_text_back": "#ffffff",
                "text_focusin_bottom_line": "#3584e4",
                "text_focusin_bottom_width": 0,
            }
        )


class GTkDarkTextBox(GTkTextBox):
    def default_palette(self):
        self.palette_gtk_dark()


if __name__ == '__main__':
    from tkinter import Tk
    from tkadw import GTkFrame, GTkDarkFrame, GTkButton, GTkDarkButton, GTkEntry, GTkDarkEntry

    root = Tk()
    root.configure(background="#1f1f1f")

    frame = GTkFrame(root)

    button1 = GTkButton(frame.frame, text="GTkButton")
    button1.pack(fill="x", ipadx=5, padx=5, pady=5)

    entry1 = GTkEntry(frame.frame)
    entry1.pack(fill="x", ipadx=5, padx=5, pady=5)

    textbox1 = GTkTextBox(frame.frame)
    textbox1.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame.pack(fill="both", expand="yes", side="right")

    frame2 = GTkDarkFrame(root)

    button2 = GTkDarkButton(frame2.frame, text="GTkDarkButton")
    button2.pack(fill="x", ipadx=5, padx=5, pady=5)

    entry2 = GTkDarkEntry(frame2.frame)
    entry2.pack(fill="x", ipadx=5, padx=5, pady=5)

    textbox2 = GTkDarkTextBox(frame2.frame)
    textbox2.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame2.pack(fill="both", expand="yes", side="left")

    root.mainloop()
