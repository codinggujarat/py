'''A simple GUI application that allows users to
open and view images'''
import tkinter as tk
from tkinter import Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

def image_viewer():
    root = tk.Tk()
    root.title("Image Viewer")

    def open_image():
        file_path = askopenfilename()
        if file_path:  # Check if a file was selected
            img = Image.open(file_path)
            img = img.resize((350, 350), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection

    button = Button(root, text="Open Image", command=open_image)
    button.pack()
    label = Label(root)
    label.pack()
    root.mainloop()

image_viewer()