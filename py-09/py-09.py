""" This program is a recursive solution to calculate the number of possible ways a character can traverse a given terrain represented by a string of dashes (`-`) and carats (`^`). The character can only move forward, stepping one space at a time or jumping two spaces. The goal is to determine all valid paths across the terrain for each line in a file (`paths.txt`) and output the results.

### Key Points:
1. **Terrain Representation**:
    - `-` represents smooth ground where the character can step or jump.
    - `^` represents an obstacle that the character can only jump over.

2. **Recursive Approach**:
    - The program uses recursion to explore all possible paths across the terrain.
    - At each position, the character can either:
      - Step forward by 1 space (if the next space is `-`).
      - Jump forward by 2 spaces (if the space after the next is `-`).

3. **Input**:
    - The program reads multiple terrains from a file (`paths.txt`), where each line represents a terrain.

4. **Output**:
    - For each terrain, the program outputs the number of valid ways to traverse it.

5. **Constraints**:
    - The program must use recursion to explore all possible paths.
    - It must handle multiple terrains and output the results in a clear format.

6. **Example**:
    For the terrain `-^-^-^-^---^-----^---`, the program calculates all valid paths (e.g., combinations of steps and jumps) and outputs the total count.

HAD TO GET AN AI TO RE-EXPLAIN THE Meaning of this ^^^
ASSISTED WITH GITHUB COPILOT
 """
import os
 
def count_paths(terrain, position=0):
    """Recursively count the number of valid paths through the terrain."""
    # Base case: if we reach the end of the terrain, return 1 (valid path found)
    if position >= len(terrain):
        return 1
    
    # If the current position is an obstacle, return 0 (invalid path)
    if terrain[position] == '^':
        return 0
    
    # Count paths by stepping (1 space) and jumping (2 spaces)
    step = count_paths(terrain, position + 1)  # Step forward by 1
    jump = count_paths(terrain, position + 2)  # Jump forward by 2
    
    return step + jump
 
def process_terrains(file_path):
    """Process each terrain in the input file and print the number of ways to traverse it."""
    try:
        with open(file_path, 'r') as file:
            terrains = file.readlines()
            
        for i, terrain in enumerate(terrains):
            terrain = terrain.strip()  # Remove any trailing whitespace or newline characters
            if terrain:  # Skip empty lines
                paths_count = count_paths(terrain)
                print(f"Path: :{terrain}")
                print(f"Terrain {i + 1}: {paths_count} Number of ways to traverse") # IT EVEN PREDICTED THAT I WOULD USE TRAVERSE.
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")    

if __name__ == "__main__":
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the input file containing terrains
    input_file = os.path.join(script_dir, "paths.txt")
    
    process_terrains(input_file)