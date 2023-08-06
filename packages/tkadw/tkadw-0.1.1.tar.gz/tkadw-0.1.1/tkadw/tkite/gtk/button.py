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

                "button_pressed_border": "#3584e4",
                "button_pressed_back": "#dad6d2",
                "button_pressed_text_back": "#2e3436",
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


class GTkDestructiveButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_red()


class GTkSuggestedButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_blue()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    button = GTkButton(text="GTkButton", command=lambda: print("button1 clicked"))
    button.pack(ipadx=5)

    button2 = GTkDestructiveButton(text="GTkDestructiveButton", command=lambda: print("button2 clicked"))
    button2.pack(ipadx=5)

    button3 = GTkSuggestedButton(text="GTkSuggestedButton", command=lambda: print("button3 clicked"))
    button3.pack(ipadx=5)

    root.mainloop()