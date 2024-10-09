#!/bin/python3


# https://code-b.dev/blog/gui-frameworks-for-python


import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title('Themed Widgets Example')
style = ttk.Style()
style.theme_use('clam')
label = ttk.Label(root, text="Hello, Tkinter!")
label.pack()
button = ttk.Button(root, text="Click Me")
button.pack()
root.mainloop()


# import tkinter as tk
from PIL import Image, ImageTk
root = tk.Tk()
root.title('Image Example')
image = Image.open('/home/groot/Workspaces/workspace-nieces/Python_01/res/imgs/lena.jpg')
photo = ImageTk.PhotoImage(image)
label = tk.Label(root, image=photo)
label.image = photo
label.pack()
root.mainloop()


root = tk.Tk()
root.title('Custom Styling Example')
label = tk.Label(root, text="Fancy Label", bg="purple", fg="white", font=("Helvetica", 16, "bold"))
label.pack(pady=10, padx=10)
button = tk.Button(root, text="Stylish Button", bg="green", fg="white", font=("Times New Roman", 12))
button.pack(pady=5, padx=5)
root.mainloop()


import tkinter as tk
root = tk.Tk()
root.title('Grid and Frame Example')
frame = tk.Frame(root)
frame.pack()
for i in range(3):
    for j in range(3):
        button = tk.Button(frame, text=f"Button {i},{j}")
        button.grid(row=i, column=j)
root.mainloop()


from tkinter import messagebox
root = tk.Tk()
root.title('Message Box Example')
def on_button_click():
    messagebox.showinfo(title="Information", message="This is a Tkinter message box")
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()
root.mainloop()



