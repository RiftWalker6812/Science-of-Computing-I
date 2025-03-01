from PIL import Image, ImageTk
import os

# •Read in an image file
# • Resize the image to fit the screen
# • Convert it to greyscale
# • Convert the greyscale data of each pixel into an ASCII character

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

# Global variables
image_files = []  # List of image files in the directory
selected_image = None  # Currently selected image path
resize_width = 50  # Default resize width for ASCII output
output_dir = "outputs"  # Directory for saving outputs





# --- Command Center ---
def command_center():
    """Main command-line interface loop."""
    global selected_image, resize_width
    
    print("Welcome to the Image-to-ASCII Command Center!")
    refresh_image_list()  # Initial refresh of image list
    
    while True:
        print("\nAvailable Commands:")
        print("  [list]   - List available images")
        print("  [ascii]  - Convert selected image to ASCII art")
        print("  [resize] - Set width for ASCII output (default: 50)")
        print("  [out]    - Save last ASCII output to file")
        print("  [refresh]- Refresh image list")
        print("  [exit]   - Exit the program")
        
        command = input("\nEnter a command: ").lower().strip()
        
        if command == "list":
            if not image_files:
                print("No images found in the current directory.")
            else:
                print("Available images:")
                for i, img in enumerate(image_files):
                    print(f"  {i}: {img}")
        
        elif command == "ascii":
            if not image_files:
                print("No images available. Use 'refresh' to scan the directory.")
            else:
                idx = get_selection_input(len(image_files) - 1)
                selected_image = image_files[idx]
                ascii_art = process_image_to_ascii(selected_image, resize_width)
                print(f"\nASCII Art for {selected_image}:\n")
                print(ascii_art)
