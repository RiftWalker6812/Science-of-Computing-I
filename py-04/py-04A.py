from PIL import Image
import os

# •Read in an image file
# • Resize the image to fit the screen
# • Convert it to greyscale
# • Convert the greyscale data of each pixel into an ASCII character

# To Note I did use Grok as tool to create this program

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "Images")
output_dir = os.path.join(script_dir, "outputs")

# Global variables
#image_files = []  # List of image files in the directory
selected_image = None  # Currently selected image path
resize_width = 50  # Default resize width for ASCII output
#output_dir = "outputs"  # Directory for saving outputs

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Globally returns image files
def refresh_image_list():
    """Refresh the list of image files in the 'Images' directory."""
    global image_files
    try:
        image_files = [
            os.path.join(images_dir, f)
            for f in os.listdir(images_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".rifti"))
        ]
        return image_files
    except FileNotFoundError:
        print(f"'Images' directory not found in {script_dir}. Please create it and add images.")
        image_files = []
        return []
    except Exception as e:
        print(f"Error scanning 'Images' directory: {e}")
        image_files = []
        return []

# This one is going to be going to RiftLib.py future update
def get_selection_input(max_index):
    """Get user input for selecting an image by index."""
    while True:
        try:
            n = int(input(f"Select an image (0–{max_index}): "))
            if 0 <= n <= max_index:
                return n
            else:
                print(f"Please enter a number between 0 and {max_index}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def save_ascii_output(ascii_text, filename):
    """Save ASCII art to a text file in the outputs folder."""
    base_name = os.path.basename(filename)  # Get just the filename without path
    output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_ascii.txt")
    with open(output_path, "w") as file:
        file.write(ascii_text)
    return output_path

""" def process_image_to_ascii(image_path, width=50):
    # Convert an image to ASCII art. 
    try:
        # Read and resize image
        img = Image.open(image_path).convert("RGB")
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio)
        img_resized = img.resize((width, new_height), Image.Resampling.BILINEAR)
        
        # Convert to grayscale and get pixel data
        img_gray = img_resized.convert("L")
        pixels = img_gray.getdata()
        
        # Map pixels to ASCII characters
        char_range = len(ASCII_CHARS) - 1
        ascii_art = ""
        for i, pixel in enumerate(pixels):
            char_index = int(pixel / 255 * char_range)
            ascii_art += ASCII_CHARS[char_index]
            if (i + 1) % width == 0:
                ascii_art += "\n"
        return ascii_art
    except Exception as e:
        return f"Error processing image: {e}" """

def process_image_to_ascii(image_path, output_width=80):
    """Convert an image to ASCII art."""
    try:
        # Read the image file
        img = Image.open(image_path).convert("RGB")
        
        # Resize the image to fit the screen (terminal width)
        aspect_ratio = img.height / img.width
        new_width = output_width
        new_height = int(new_width * aspect_ratio)
        img_resized = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
        
        # Convert to grayscale
        img_gray = img_resized.convert("L")
        pixels = img_gray.getdata()
        
        # Convert grayscale data to ASCII characters
        char_range = len(ASCII_CHARS) - 1
        ascii_art = ""
        for i, pixel in enumerate(pixels):
            char_index = int(pixel / 255 * char_range)  # Map 0-255 to char index
            ascii_art += ASCII_CHARS[char_index]
            if (i + 1) % new_width == 0: #TEST MARKER, NEEDS TESTING TO SEE IF REALLY NECESSARY
                ascii_art += "\n"
        return ascii_art
    
    except FileNotFoundError:
        return "Error: Image file not found."
    except Exception as e:
        return f"Error: {e}"

def save_bitmap_output(image_path, width, height):
    """Save the image as a bitmap with custom size."""
    try:
        img = Image.open(image_path).convert("RGB")
        img_resized = img.resize((width, height), Image.Resampling.BILINEAR)
        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_bitmap.bmp")
        img_resized.save(output_path, "BMP")
        return output_path
    except Exception as e:
        return f"Error saving bitmap: {e}"

# --- Command Center ---
def command_center():
    """Main command-line interface loop."""
    global selected_image, resize_width
    
    print("Welcome to the Image-to-ASCII Command Center!")
    print(f"Looking for images in: {images_dir}")
    print(f"Outputs will be saved in: {output_dir}")
    refresh_image_list()  # Initial refresh
    
    while True:
        print("\nAvailable Commands:")
        print("  [list]   - List available images")
        print("  [ascii]  - Convert selected image to ASCII art")
        print("  [resize] - Set width for ASCII output (default: 50)")
        print("  [out]    - Save last ASCII output to file")
        print("  [refresh]- Refresh image list")
        print("  [bmp]    - Save image as bitmap with custom size")
        print("  [exit]   - Exit the program")
        
        command = input("\nEnter a command: ").lower().strip()
        
        if command == "list":
            if not image_files:
                print("No images found in the 'Images' directory.")
            else:
                print("Available images:")
                for i, img in enumerate(image_files):
                    print(f"  {i}: {os.path.basename(img)}")  # Show only filename
                
        elif command == "ascii":
            if not image_files:
                print("No images available. Use 'refresh' to scan the 'Images' directory.")
            else:
                idx = get_selection_input(len(image_files) - 1)
                selected_image = image_files[idx]
                ascii_art = process_image_to_ascii(selected_image, resize_width)
                print(f"\nASCII Art for {os.path.basename(selected_image)}:\n")
                print(ascii_art)
        
        elif command == "resize":
            try:
                new_width = int(input("Enter new width (20–100 recommended): "))
                if 20 <= new_width <= 200:
                    resize_width = new_width
                    print(f"Resize width set to {resize_width}.")
                else:
                    print("Please enter a value between 20 and 200.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        
        elif command == "out":
            if selected_image and "ascii_art" in locals():
                output_path = save_ascii_output(ascii_art, selected_image)
                print(f"ASCII art saved to: {output_path}")
            else:
                print("No ASCII art to save. Generate one with 'ascii' first.")
        
        elif command == "bmp":
            if not image_files:
                print("No images available. Use 'refresh' to scan the 'Images' directory.")
            else:
                idx = get_selection_input(len(image_files) - 1)
                selected_image = image_files[idx]
                try:
                    width = int(input("Enter bitmap width (e.g., 100–1000): "))
                    height = int(input("Enter bitmap height (e.g., 100–1000): "))
                    if width > 0 and height > 0:
                        output_path = save_bitmap_output(selected_image, width, height)
                        print(f"Bitmap saved to: {output_path}")
                    else:
                        print("Width and height must be positive integers.")
                except ValueError:
                    print("Invalid input. Please enter integers for width and height.")
        
        elif command == "refresh":
            refresh_image_list()
            print(f"Image list refreshed. Found {len(image_files)} images.")
        
        elif command == "exit":
            print("Goodbye!")
            break
        
        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    command_center()