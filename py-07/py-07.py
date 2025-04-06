'''
    Password Generator with Transformers
    This script generates a password based on user input words, transforming them using a set of rules.
    
    This Code was made with assistance from Grok and GPT-4o through GitHub Copilot.   
'''

# Imports
import math
import random

def transformers_Assemble(word: str) -> str:
    """Randomly transform characters in a word."""
    
    # Combined replacements dictionary for both cases
    replacements = {
        'a': '@', 'b': '8', 'c': '©', 'd': '∂', 'e': '3', 'f': 'ƒ', 'g': '9',
        'h': '#', 'i': '1', 'j': ']', 'k': 'κ', 'l': '|', 'm': '^^', 'n': '∩',
        'o': '0', 'p': 'ρ', 'q': '¶', 'r': 'π', 's': '$', 't': 'τ', 'u': 'μ',
        'v': '√', 'w': 'ω', 'x': '×', 'y': '¥', 'z': '2'
    }

    transformed = []
    for char in word:
        if random.random() < math.pi:  # pi% chance to transform
            # Transform the character if it's in the replacements dictionary
            transformed_char = replacements.get(char.lower(), char)
            # Randomly decide to uppercase the transformed character
            if random.random() < 0.5:
                transformed_char = transformed_char.upper()
            transformed.append(transformed_char)
        else:
            # Keep the character as is (lowercase)
            transformed.append(char.lower())

    return ''.join(transformed)

def generate_password():
    # Step 1: Input collection
    words = [str]
    words = str(input("Enter 3 words (at least 3 letters each, separated by spaces): ")).strip().split()
    
    # Step 2: Check word list length
    if len(words) < 3:
        print("You had the nerve to write less than 3 words.\nNow the pc will crash.")
        exit(1)
    elif len(words) > 3:
        print("Someone is trying to be smart.\nthree was never enough.")
        
    # Shuffle
    random.shuffle(words)
    
    # Step 3: Transform each word
    String_Mutation = [transformers_Assemble(word) for word in words]  
        
    # Step 4: check and change double letters
    # by swapping one of the double letters with a random character thats not the same
    def remove_double_letters(password: str) -> str:
        """Replace consecutive duplicate letters with a random character."""
        result = []
        for i, char in enumerate(password):
            if i > 0 and char == password[i - 1]:  # Check for consecutive duplicates
                # Generate a random replacement character that is not the same
                replacement = char
                while replacement == char:
                    replacement = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()")
                result.append(replacement)
            else:
                result.append(char)
        return ''.join(result)  
     
     # Step 5: Remove double letters
    String_Mutation = [remove_double_letters(word) for word in String_Mutation]   
        
    final_password = ''.join(String_Mutation)
    print(f"Generated password: {final_password}")
    if 'π' in final_password:
        print("The password contains the letter π, which is a special character.")
        
                
if __name__ == "__main__":
    generate_password()