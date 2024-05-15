import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import itertools

rat_image = Image.open('rat.png')

# Initialize global variables for rotation
transformed_image = None
tk_image = None
angle = 0
showing = False
# colours for flashing text
flashing_colours = ['red', 'green', 'blue', 'yellow', 'black', 'white']

def colourize_image(image, colour):
    gray_image = ImageOps.grayscale(image)
    rgb_image = gray_image.convert("RGB")
    coloured_image = ImageEnhance.Color(rgb_image).enhance(2)
    return ImageOps.colorize(gray_image, black="black", white=colour)

def show_rat(selected_colour):
    global transformed_image, tk_image, showing, angle
    if (showing == False):
        transformed_image = colourize_image(rat_image, selected_colour)
        tk_image = ImageTk.PhotoImage(transformed_image)
        canvas.image = tk_image  
        canvas.itemconfig(image_id, image=tk_image)
        
        angle = 0
        rotate_image()
        flash_text()
        showing = True

def rotate_image():
    global angle 
    rotated = transformed_image.rotate(angle)
    tk_image_rotated = ImageTk.PhotoImage(rotated)
    canvas.image = tk_image_rotated
    canvas.itemconfig(image_id, image=tk_image_rotated)
    angle = (angle + 20) % 360
    root.after(50, rotate_image)

def flash_text():
    current_colour = next(colour_cycle)
    text_label.config(fg=current_colour)
    root.after(500, flash_text)

def on_submit():
    selected_colour = colour_var.get()
    show_rat(selected_colour)

root = tk.Tk()
root.title("Rat Colour Selector")
root.geometry("400x400")


colour_var = tk.StringVar()
colour_combobox = ttk.Combobox(root, textvariable=colour_var)
colour_combobox['values'] = ('Red', 'Green', 'Blue', 'Yellow', 'White')
colour_combobox.pack(pady=10)

submit_button = ttk.Button(root, text="Show Rat Colour", command=on_submit)
submit_button.pack(pady=10)

# canvas
canvas = tk.Canvas(root, width=rat_image.width, height=rat_image.height)
canvas.pack(pady=10)
image_id = canvas.create_image(rat_image.width // 2, rat_image.height // 2, anchor=tk.CENTER)

# flashing text
text_label = tk.Label(root, text="Rat gang!", font=("Courier", 34))
text_label.pack(pady=10)
colour_cycle = itertools.cycle(flashing_colours)


root.mainloop()
