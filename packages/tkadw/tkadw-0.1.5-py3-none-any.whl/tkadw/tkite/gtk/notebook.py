from tkinter import Frame
from tkadw import AdwDrawEngine


class GTkNoteBook(AdwDrawEngine):
    def __init__(self, bg="#e1dedb"):
        super().__init__(bg=bg, bd=0)

        self.bind("<Configure>", lambda event: self.__draw())

        self.tabs = {
            "Tab1":
        }

    def __draw(self):


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()

    notebook = GTkNoteBook()
    notebook.pack(fill="both", expand="yes")

    root.mainloop()