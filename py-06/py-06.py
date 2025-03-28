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

class Record_Data(NamedTuple):
    year: int
    name: str
    location: str
    value_dat: str
    extra: str

Datas_List: dict[int, list[Record_Data]] = {}
title, x_axis, source = str, str, str

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
def read_and_parse_text_file(filename: str):
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
        print(f"Contents of {file_path.name}:\n{content}\n")

        # Parse the file content
        lines = content.strip().split("\n")
        
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


def main():
    try:
        
        file_name_data = get_text_filenames()
        if file_name_data is False:
            print("Not Data Exists in Data Folder")
            raise ValueError("No Data")
        
        for i in range(len(file_name_data) - 1):
            print(f"{i}: {file_name_data[i]}")
        
        User_Select = int(input("Select a data file you want displayed (Int): "))
        read_and_parse_text_file(file_name_data[User_Select])
        
        """ print("Data in Datas_List:")
        for year, records in Datas_List.items():
            print(f"Year {year}:")
            for record in records:
                print(f"  {record.name}, {record.location}, {record.value_dat}, {record.extra}")
 """    
        # How many Bars
        
        # Setup Bars
        chart = BarChart(title, x_axis, source)
        for Years_dat, Records_Dat in Datas_List.items():
            chart.set_caption(Years_dat)
            for rec in Records_Dat: # Remake to set bars up to 10
                chart.add(f'{rec.name}, {rec.location}',    rec.value_dat, rec.extra)
 
    except FileNotFoundError as e:
        print(e)    
    
    
    
if __name__ == '__main__':
    main()
