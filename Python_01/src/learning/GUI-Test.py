#!/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Image as ImageTk
from PIL import Image, ImageTk

root = tk.Tk()

images = "./res/imgs/"

root.title('Themed Widgets Example')
style = ttk.Style()
style.theme_use('clam')
label = ttk.Label(root, text="Hello, Tkinter!")
label.pack()

frame1 = tk.Frame(root)
frame1.pack()

imge = Image.open(images + 'vulkanlogo.png')
phot = ImageTk.PhotoImage(imge)
button = ttk.Button(frame1, text="Click Me", image=phot)
button.grid(row=0,column=0)
# button.pack()

root.title('Image Example')
image = Image.open(images + 'lena.jpg')
photo = ImageTk.PhotoImage(image)
label = tk.Label(frame1, image=photo)
label.grid(row=0,column=1)
# label.pack()
label = ttk.Label(root, text="TESTING")
label.pack()

root.title('Custom Styling Example')
label = tk.Label(root, text="Fancy Label", bg="Navy", fg="white", font=("Helvetica", 26, "bold"))
label.pack(pady=10, padx=10)
button = tk.Button(root, text="Stylish Button", bg="green", fg="white", font=("Times New Roman", 12))
button.pack(pady=5, padx=5)


root.title('Grid and Frame Example')

frame = tk.Frame(root)
frame.pack()
for i in range(3):
    for j in range(5):
        button = tk.Button(frame, text=f"Button {i},{j}")
        button.grid(row=i, column=j)

root.title('Message Box Example')
def on_button_click():
    messagebox.showinfo(title="Information", message="This is a Tkinter message box")
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()

root.mainloop()
