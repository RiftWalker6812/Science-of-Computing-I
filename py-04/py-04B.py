import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
from PIL import Image, ImageTk
import os

# Window setup with drag-and-drop support
window = TkinterDnD.Tk()
window.title("Image Processor")
window.geometry("900x600")

# Global variables
image_files = []  # List to store image paths
current_image = None  # Current selected image

# ASCII character set
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

# --- Functions ---
def process_image(image_path, mode="pixel", resolution=50):
    """Process the image into ASCII or pixelated form."""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    aspect_ratio = height / width
    
    # Adjust resolution based on mode
    if mode == "ascii":
        # Smaller resolution for ASCII (20-80 chars wide makes sense)
        new_width = max(20, min(resolution, 80))  # Cap between 20 and 80
        new_height = int(new_width * aspect_ratio)
        img_resized = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
        pixels = img_resized.convert("L").getdata()  # Grayscale
        ascii_img = ""
        char_range = len(ASCII_CHARS) - 1
        for i, pixel in enumerate(pixels):
            char_index = int(pixel / 255 * char_range)  # Map 0-255 to char index
            ascii_img += ASCII_CHARS[char_index]
            if (i + 1) % new_width == 0:
                ascii_img += "\n"
        return ascii_img
    else:
        # Pixel mode can use higher resolution
        new_width = resolution
        new_height = int(new_width * aspect_ratio)
        img_resized = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
        return img_resized.resize((width, height), Image.Resampling.NEAREST)

def update_output():
    """Update the output box based on selected image and mode."""
    if current_image:
        mode = mode_var.get()
        resolution = int(resolution_var.get())
        if mode == "ascii":
            ascii_text = process_image(current_image, mode="ascii", resolution=resolution)
            output_label.config(text=ascii_text, image="", font=("Courier", 10), justify=tk.LEFT)
        else:
            processed_img = process_image(current_image, mode="pixel", resolution=resolution)
            photo = ImageTk.PhotoImage(processed_img)
            output_label.config(image=photo, text="")
            output_label.image = photo  # Keep reference to avoid garbage collection

def drop(event):
    """Handle dropped files."""
    files = window.tk.splitlist(event.data)
    for file in files:
        if file.endswith((".png", ".jpg", ".jpeg")):
            image_files.append(file)
            image_listbox.insert(tk.END, os.path.basename(file))
    if image_files and not current_image:
        select_image(0)

def select_image(event=None):
    """Update current image when clicked in listbox."""
    global current_image
    selection = image_listbox.curselection()
    if selection:
        index = selection[0]
        current_image = image_files[index]
        update_output()

# --- GUI Layout ---
# Left: Drag-and-drop area
drop_frame = tk.Frame(window, width=200, height=400, bg="lightgray", relief="sunken")
drop_frame.pack(side=tk.LEFT, padx=10, pady=10)
drop_label = tk.Label(drop_frame, text="Drag Images Here", bg="lightgray")
drop_label.pack(expand=True)
drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)

# Middle: Output display
output_frame = tk.Frame(window, width=400, height=400, bg="white", relief="sunken")
output_frame.pack(side=tk.LEFT, padx=10, pady=10)
output_label = tk.Label(output_frame, bg="white")
output_label.pack(expand=True)

# Right: Image list
list_frame = tk.Frame(window, width=200, height=400, bg="lightgray", relief="sunken")
list_frame.pack(side=tk.LEFT, padx=10, pady=10)
image_listbox = tk.Listbox(list_frame, height=20)
image_listbox.pack(fill=tk.BOTH, expand=True)
image_listbox.bind('<<ListboxSelect>>', select_image)

# Controls below
control_frame = tk.Frame(window)
control_frame.pack(side=tk.BOTTOM, pady=10)

mode_var = tk.StringVar(value="pixel")
tk.Label(control_frame, text="Output Mode:").pack(side=tk.LEFT)
tk.Radiobutton(control_frame, text="Pixel", variable=mode_var, value="pixel", command=update_output).pack(side=tk.LEFT)
tk.Radiobutton(control_frame, text="ASCII", variable=mode_var, value="ascii", command=update_output).pack(side=tk.LEFT)

resolution_var = tk.StringVar(value="50")
tk.Label(control_frame, text="Resolution:").pack(side=tk.LEFT, padx=(10, 0))
tk.Entry(control_frame, textvariable=resolution_var, width=5).pack(side=tk.LEFT)
tk.Button(control_frame, text="Update", command=update_output).pack(side=tk.LEFT, padx=5)

# Start the app
window.mainloop()