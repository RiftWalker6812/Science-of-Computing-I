from PIL import Image, ImageTk
import os

# •Read in an image file
# • Resize the image to fit the screen
# • Convert it to greyscale
# • Convert the greyscale data of each pixel into an ASCII character

# Create a List of image files (Needs refresh command)

#Get Selection input via int and return image
def get_selection_Input():
    N: str
    while True:
        try:
            N = int(input("Select an image via inputing an integer: "))
            if 101 <= N:
                continue
            break
        except ValueError as e:
            print(f"{e} try again")
    return N


ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]
Selected_Image: str

# Get all file names in directory

# Command Center
print("Welcome to the command center, type in a commnd")
while True:
    print("[List] List Images Available\n[Ascii] Gets an ascii of an availbe image\n[Rezise] Set Rezise fo output\n[out] outputs last image into outputs folder\n[Exit] Exits Program")




with open(Selected_Image, "wb") as file:
        file.write(encrypted)