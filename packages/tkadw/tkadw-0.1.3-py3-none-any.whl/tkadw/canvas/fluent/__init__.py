from tkadw.canvas.drawengine import AdwDrawEngine
from tkinter import Frame


class AdwFluentAppBar(Frame):
    def __init__(self, *args, width=360, height=80, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.configure(background="#ffffff")

    def show(self):
        self.pack(fill="x", side="top")


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    appbar = AdwFluentAppBar()
    appbar.show()

    root.mainloop()