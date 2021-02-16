from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('Testing editor textpad')
root.geometry("1200x600")

frame = Frame(root)
frame.pack(pady=5)

text = Text(frame, width=97, height=25, font=("Helvetica",16), selectbackground="yellow", selectforeground="black", undo="True")
text.pack()


root.mainloop()