from tkadw.canvas.button import AdwDrawBasicRoundButton
from tkinter.font import Font, families, nametofont

WHITE = "#ffffff"
BLACK = "#000000"

SURFACE1 = "#f8f8f8"
SURFACE2 = "#f3f3f4"

PRIMARY25 = "#f9f8ff"
PRIMARY50 = "#f1eeff"
PRIMARY75 = "#e2dcff"
PRIMARY100 = "#c6bbff"
PRIMARY200 = "#bcafff"
PRIMARY300 = "#a797ff"
PRIMARY400 = "#8b75ff"
PRIMARY500 = "#7357ff"
PRIMARY600 = "#6347f4"
PRIMARY700 = "#553ade"
PRIMARY800 = "#3c28a4"
PRIMARY900 = "#21194d"

PRIMARY_ACCENT1 = PRIMARY50
PRIMARY_ACCENT2 = PRIMARY75

LOW_EM = "#ececed"
MED_EM = "#4f4b5c"


class AdwAtomizeButton(AdwDrawBasicRoundButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _draw(self, evt=None):
        super()._draw(evt)

        self.itemconfigure(self.button_frame, width=3)

    def default_palette(self):
        self.palette(
            {
                "button_radius": 100,

                "button_border_width": 1,

                "button_border": WHITE,
                "button_back": WHITE,
                "button_text_back": MED_EM,

                "button_active_border": SURFACE2,
                "button_active_back": SURFACE2,
                "button_active_text_back": MED_EM,

                "button_pressed_border": SURFACE1,
                "button_pressed_back": SURFACE1,
                "button_pressed_text_back": PRIMARY700,
            }
        )

    def accent_palette(self):
        self.palette(
            {
                "button_radius": 100,

                "button_border_width": 2,

                "button_border": PRIMARY500,
                "button_back": PRIMARY500,
                "button_text_back": WHITE,

                "button_active_border": PRIMARY400,
                "button_active_back": PRIMARY400,
                "button_active_text_back": WHITE,

                "button_pressed_border": PRIMARY200,
                "button_pressed_back": PRIMARY400,
                "button_pressed_text_back": WHITE,
            }
        )


class AdwAtomizeAccentButton(AdwAtomizeButton):
    def default_palette(self):
        self.accent_palette()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    button1 = AdwAtomizeButton()
    button1.pack(padx=5, pady=5, fill="both", expand="yes")

    button2 = AdwAtomizeAccentButton()
    button2.pack(padx=5, pady=5, fill="both", expand="yes")

    root.mainloop()
