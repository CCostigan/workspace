#!/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Image as ImageTk
from PIL import Image, ImageTk


class GuiThread():
    def __init__(self, root):

        self.root = root  #tk.Tk()

    def start(self):

        self.images = "./resources/imgs/"

        self.root.title('Themed Widgets Example')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        label = ttk.Label(self.root, text="Hello, Tkinter!")
        label.pack()

        self.frame1 = tk.Frame(self.root)
        self.frame1.pack()

        imge = Image.open(self.images + 'vulkanlogo.png')
        phot = ImageTk.PhotoImage(imge)
        button = ttk.Button(self.frame1, text="Click Me", image=phot)
        button.grid(row=0,column=0)
        # button.pack()

        self.root.title('Image Example')
        image = Image.open(self.images + 'lena.jpg')
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.frame1, image=photo)
        label.grid(row=0,column=1)
        # label.pack()
        label = ttk.Label(self.root, text="TESTING")
        label.pack()

        self.root.title('Custom Styling Example')
        label = tk.Label(self.root, text="Fancy Label", bg="Navy", fg="white", font=("Helvetica", 26, "bold"))
        label.pack(pady=10, padx=10)
        button = tk.Button(self.root, text="Stylish Button", bg="green", fg="white", font=("Times New Roman", 12))
        button.pack(pady=5, padx=5)


        self.root.title('Grid and self.frame Example')

        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for i in range(3):
            for j in range(5):
                button = tk.Button(self.frame, text=f"Button {i},{j}")
                button.grid(row=i, column=j)

        self.root.title('Message Box Example')
        def on_button_click():
            messagebox.showinfo(title="Information", message="This is a Tkinter message box")
        button = tk.Button(self.root, text="Click Me", command=on_button_click)
        button.pack()

from GUI_Test import GuiMain
if __name__ == '__main__':
    gt = GuiMain()
    gt.start_thread()
