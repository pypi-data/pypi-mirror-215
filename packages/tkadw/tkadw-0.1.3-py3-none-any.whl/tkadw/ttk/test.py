from tkadw.ttk.atomize_ttk import use_light_theme
from tkinter import Tk
from tkinter import ttk


root = Tk()

use_light_theme()

frame = ttk.Frame(style="Card.TFrame")
frame.pack(fill="both", padx=5, pady=5)

button = ttk.Button(frame, style="Accent.TButton", command=lambda: print("hello world"))
button.pack(fill="both", padx=5, pady=5)

root.mainloop()