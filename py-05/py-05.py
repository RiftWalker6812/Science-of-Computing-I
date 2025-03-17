

""" 
• The user is allowed to use the following operators: +, -, *, /, ^ (exponent).
• No ()’s in the equations to solve – we’ll deal with those in another program.
• Don’t worry about negative numbers as input either (not yet anyway).
• Using the order of operations (aka: PEMDAS), output the correct result. 
"""
# Assisted with Grok

def IsValidString(input_String):
    # math symbols allowed
    Math_Symbols = {'+', '-', '*', '/', '^'}
    
    # Checks to see all chars are valid
    has_a_valid_symbol = all(
    not char.isalpha() or 
    char.isdigit() or 
    char in Math_Symbols or 
    not char.isspace()
    for char in input_String)
    
    # Checks for adjacent symbols
    adjacent_validity = True
    

def Main():
    print("5 FUnction Calculator")
    UserInput = input("Input math, EX: 5+5").strip
    if UserInpu

if __name__ == "__main__":
    Main()