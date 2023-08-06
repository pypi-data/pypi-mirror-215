from tkinter import Tk
from tkadw import GTkFrame, GTkDarkFrame, GTkButton, GTkDarkButton, GTkEntry, GTkDarkEntry, GTkTextBox, GTkDarkTextBox

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
