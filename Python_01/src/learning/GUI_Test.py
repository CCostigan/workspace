#!/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Image as ImageTk
from PIL import Image, ImageTk

import logging
from logging.config import fileConfig

from GUI_Thread import GuiThread

# Static variables not part of class but visible to it
fileConfig('./resources/cfg/alogger.cfg')        
logger = logging.getLogger(__file__)

class GuiMain():
    # Class variables (shared by all instances)
    log = logging.getLogger(__file__)

    def __init__(self):
        # Instance variables (unique per instance)
        self.root = tk.Tk()

    def start_thread(self):
        logger.info("Starting")
        gt = GuiThread(self.root)
        gt.start()
        self.root.mainloop()
        logger.info("Done...")


    def start_old(self):

        images = "./resources/imgs/"

        # self.root.title('Themed Widgets Example')
        # style = ttk.Style()
        # style.theme_use('clam')
        # label = ttk.Label(self.root, text="Hello, Tkinter!")
        # label.pack()

        # frame1 = tk.Frame(self.root)
        # frame1.pack()

        # imge = Image.open(images + 'vulkanlogo.png')
        # phot = ImageTk.PhotoImage(imge)
        # button = ttk.Button(frame1, text="Click Me", image=phot)
        # button.grid(row=0,column=0)
        # # button.pack()

        # self.root.title('Image Example')
        # image = Image.open(images + 'lena.jpg')
        # photo = ImageTk.PhotoImage(image)
        # label = tk.Label(frame1, image=photo)
        # label.grid(row=0,column=1)
        # # label.pack()
        # label = ttk.Label(self.root, text="TESTING")
        # label.pack()

        # self.root.title('Custom Styling Example')
        # label = tk.Label(self.root, text="Fancy Label", bg="Navy", fg="white", font=("Helvetica", 26, "bold"))
        # label.pack(pady=10, padx=10)
        # button = tk.Button(self.root, text="Stylish Button", bg="green", fg="white", font=("Times New Roman", 12))
        # button.pack(pady=5, padx=5)


        # self.root.title('Grid and Frame Example')

        # frame = tk.Frame(self.root)
        # frame.pack()
        # for i in range(3):
        #     for j in range(5):
        #         button = tk.Button(frame, text=f"Button {i},{j}")
        #         button.grid(row=i, column=j)

        # self.root.title('Message Box Example')
        # def on_button_click():
        #     messagebox.showinfo(title="Information", message="This is a Tkinter message box")
        # button = tk.Button(self.root, text="Click Me", command=on_button_click)
        # button.pack()

        # self.root.mainloop()

if __name__ == '__main__':
    wapp = GuiMain()
    # wapp.start_old()
    wapp.start_thread()
