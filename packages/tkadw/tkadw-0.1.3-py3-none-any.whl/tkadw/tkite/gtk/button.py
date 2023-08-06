from tkadw import AdwDrawRoundButton3


class GTkButton(AdwDrawRoundButton3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "button_radius": 11,

                "button_border_width": 1.3,

                "button_border": "#ccc6c1",
                "button_back": "#f6f5f4",
                "button_text_back": "#2e3436",

                "button_active_border": "#dad6d2",
                "button_active_back": "#f8f8f7",
                "button_active_text_back": "#2e3436",

                "button_pressed_border": "#dad6d2",
                "button_pressed_back": "#dad6d2",
                "button_pressed_text_back": "#2e3436",
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "button_radius": 11,

                "button_border_width": 1.3,

                "button_border": "#1b1b1b",
                "button_back": "#353535",
                "button_text_back": "#eeeeec",

                "button_active_border": "#1b1b1b",
                "button_active_back": "#373737",
                "button_active_text_back": "#eeeeec",

                "button_pressed_border": "#282828",
                "button_pressed_back": "#1e1e1e",
                "button_pressed_text_back": "#eeeeec",
            }
        )

    def palette_gtk_red(self):
        self.palette(
            {
                "button_radius": 11,

                "button_border_width": 1.3,

                "button_border": "#851015",
                "button_back": "#d81a23",
                "button_text_back": "#ffffff",

                "button_active_border": "#9c1319",
                "button_active_back": "#bc171e",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#9c1319",
                "button_pressed_back": "#a0131a",
                "button_pressed_text_back": "#ffffff",
            }
        )

    def palette_gtk_blue(self):
        self.palette(
            {
                "button_radius": 11,

                "button_border_width": 1.3,

                "button_border": "#15539e",
                "button_back": "#2d7fe3",
                "button_text_back": "#ffffff",

                "button_active_border": "#185fb4",
                "button_active_back": "#1a65c2",
                "button_active_text_back": "#ffffff",

                "button_pressed_border": "#185fb4",
                "button_pressed_back": "#1961b9",
                "button_pressed_text_back": "#ffffff",
            }
        )


class GTkDarkButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_dark()


class GTkDestructiveButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_red()


class GTkSuggestedButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_blue()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.configure(background="#1e1e1e")

    button = GTkDarkButton(text="GTkButton", command=lambda: print("button1 clicked"))
    button.pack(fill="x", ipadx=5, padx=5, pady=5)

    button2 = GTkDarkButton(text="GTkDarkButton", command=lambda: print("button2 clicked"), background="#1e1e1e")
    button2.pack(fill="x", ipadx=5, padx=5, pady=5)

    button3 = GTkDestructiveButton(text="GTkDestructiveButton", command=lambda: print("button3 clicked"))
    button3.pack(fill="x", ipadx=5, padx=5, pady=5)

    button4 = GTkSuggestedButton(text="GTkSuggestedButton", command=lambda: print("button4 clicked"))
    button4.pack(fill="x", ipadx=5, padx=5, pady=5)

    root.mainloop()