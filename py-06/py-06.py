'''
1. Ask the user for the data file and how many bars to display.
2. Skip the header lines in the file.
3. Read data from a file into a Dictionary. (Read in only one group, not the whole file.)
4. Sort the Dictionary by the value of each record (1 record = 1 line of data).
5. Create and display a (static, not moving) bar chart.
6. Pause a bit.
7. Repeat steps 3 – 6 until the file is done
'''

'''
data is recorded as year, numb, text [grouped by year]
need a dictionary of years holding lists which when called need be sorted


Dict: year, List[Record_Data]

'''


from BarChart import BarChart
from typing import NamedTuple
from pathlib import Path
import matplotlib
import time

class Record_Data(NamedTuple):
    year: int
    name: str
    location: str
    value_dat: str
    extra: str

Datas_List: dict[int, list[Record_Data]] = {}
title: str = ""
x_axis: str = ""
source: str = ""

 # Get the directory of the current script
script_dir = Path(__file__).parent
data_folder = script_dir / "Data"
#Datas_folder = Path("Data")

def get_text_filenames():
    """
    Returns a list of all .txt filenames in the specified folder.
    """
    #data_folder = Path(data_folder)
    
    if not data_folder.exists() or not data_folder.is_dir():
        raise FileNotFoundError(f"The '{data_folder}' folder does not exist or is not a directory.")
    
    # List all .txt files
    filenames = [f.name for f in data_folder.glob("*.txt")]
    return filenames

# AAAAA
def read_and_parse_text_file(filename: str) -> None:
    """
    Reads and parses a single specified .txt file from the folder, 
    storing the parsed data into Datas_List by year.
    Returns the raw content of the file as a string.
    """
    # Construct the full path to the Data folder and file
    
    file_path = data_folder / filename
    # Check if the file exists
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"The file '{file_path}' does not exist or is not a file.")
    
    content = str
    # Read the file # GROK HELPED ME HERE, I HATE NON JSON's
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        #print(f"Contents of {file_path.name}:\n{content}\n")

        # Parse the file content
        lines = content.strip().split("\n")
        
        global title, x_axis, source
        title, x_axis, source = lines[0], lines[1], lines[2]
        
        i = 0
        while i < len(lines):
            # Skip header lines until we hit a number (e.g., "27" or "12")
            if not lines[i].strip().isdigit():
                i += 1
                continue
            
            # Get the number of data lines to process
            num_entries = int(lines[i].strip())
            i += 1  # Move to the first data line

            # Process the next `num_entries` lines
            for j in range(num_entries): # starts with 0 
                if i + j >= len(lines): 
                    break  # Avoid index out of range
                line = lines[i + j].strip() # index + 0 init -> index + next entry
                if not line:
                    continue  # Skip empty lines

                # Split the comma-separated data
                fields = [f.strip() for f in line.split(",")]
                if len(fields) < 5:
                    print(f"Skipping malformed line in {file_path.name}: {line}")
                    continue

                # Extract fields based on data type (movies or cities)
                date_or_year, name, country, value, Extra = fields[:5] # ITS ADVANCED
                
                # Determine year (movies have "YYYY-MM-DD", cities have "YYYY")
                if "-" in date_or_year:
                    Year = int(date_or_year.split("-")[0])  # e.g., "1982-01-14" → 1982
                else:
                    Year = int(date_or_year)  # e.g., "1500"

                # Create Record_Data object
                record = Record_Data(
                    year=Year,
                    name=name,
                    location=country,
                    value_dat=value,  # Kept as string
                    extra=Extra
                )

                # Add to Datas_List # doesnt feel right
                if Year not in Datas_List:
                    Datas_List[Year] = []
                Datas_List[Year].append(record)

            i += num_entries  # Move past this block of data

    return #content

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main(): # My function
    try:
        
         # Get available files
        file_names = get_text_filenames()
        if not file_names:
            print("No .txt files found in Data folder.")
            return
        
        # Display file options
        for i, name in enumerate(file_names):
            print(f"{i}: {name}")
        
        # User selects file
        user_select = int(input("Select a data file by number: "))
        if user_select < 0 or user_select >= len(file_names):
            raise ValueError("Invalid file selection.")
        
         # Parse the selected file
        read_and_parse_text_file(file_names[user_select])
        
        # Get number of bars from user
        number_of_bars = int(input("Input number of bars to display (max 10): "))
        if number_of_bars > 10:
            number_of_bars = 10  # Cap at 10
            
        # Setup Bars
        chart = BarChart(title, x_axis, source)
        
        # Process each year’s data
        for year, records in Datas_List.items():
            # Sort by value_dat numerically (convert to int)
            sorted_records = sorted(records, key=lambda r: int(r.value_dat), reverse=True)
            chart.reset()  # Clear previous bars
            chart.set_caption(str(year))
            
            # Add top N records (up to number_of_bars)
            for rec in sorted_records[:number_of_bars]:
                chart.add(f"{rec.name}, {rec.location}", int(rec.value_dat), rec.extra)
            
            chart.draw()    
            time.sleep(.35)
        chart.leave_window_open()

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")      
    
def better_main(): # THIS ONE IS BEYOND ME AS IT WORKS WITH ANIMATIONS
    try:
        # Get available files
        file_names = get_text_filenames()
        if not file_names:
            print("No .txt files found in Data folder.")
            return
        
        # Display file options
        for i, name in enumerate(file_names):
            print(f"{i}: {name}")
        
        # User selects file
        user_select = int(input("Select a data file by number: "))
        if user_select < 0 or user_select >= len(file_names):
            raise ValueError("Invalid file selection.")
        
        # Parse the selected file
        read_and_parse_text_file(file_names[user_select])
        
        # Get number of bars from user
        number_of_bars = min(int(input("Input number of bars to display (max 10): ")), 10)
        
        # Prepare data
        sorted_data = {
            year: sorted(records, key=lambda r: int(r.value_dat), reverse=True)[:number_of_bars]
            for year, records in Datas_List.items()
        }
        years = list(sorted_data.keys())

        # Setup chart
        chart = BarChart(title, x_axis, source)
        
        # Animation function
        def update(frame):
            chart.reset()
            year = years[frame % len(years)]
            chart.set_caption(str(year))
            for rec in sorted_data[year]:
                chart.add(f"{rec.name}, {rec.location}", int(rec.value_dat), rec.extra)
            chart.draw()
            return chart.fig.gca(),  # Return the updated axes

        # Create animation
        ani = FuncAnimation(
            chart.fig,          # The figure to animate
            update,             # Function to call for each frame
            frames=len(years),  # Number of frames (one per year)
            interval=250,      # Delay between frames in milliseconds (2 seconds)
            repeat=True         # Loop the animation
        )
        
        chart.leave_window_open()  # Keep the window open

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    
if __name__ == '__main__':
    main()
