from tkadw.canvas.button import AdwDrawRoundButton, AdwDrawRoundButton2, AdwDrawRoundButton3
from tkinter.font import Font, families, nametofont

WHITE = "#ffffff"
BLACK = "#000000"

PRIMARY = "#41118E"
PRIMARY_HOVER = "#4D16A4"
PRIMARY_PRESSED = "#3B0F82"


class AdwAtomizeButton(AdwDrawRoundButton3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _draw(self, evt=None):
        super()._draw(evt)

        self.itemconfigure(self.button_frame, width=3)

    def default_palette(self):
        self.palette(
            {
                "button_radius": 9,

                "button_border_width": 0,

                "button_border": PRIMARY,
                "button_back": PRIMARY,
                "button_text_back": WHITE,

                "button_active_border": PRIMARY_HOVER,
                "button_active_back": PRIMARY_HOVER,
                "button_active_text_back": WHITE,

                "button_pressed_border": PRIMARY_PRESSED,
                "button_pressed_back": PRIMARY_PRESSED,
                "button_pressed_text_back": WHITE,
            }
        )


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    button1 = AdwAtomizeButton()
    button1.pack(padx=5, pady=5, fill="both", expand="yes")

    root.mainloop()
