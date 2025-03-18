

""" 
• The user is allowed to use the following operators: +, -, *, /, ^ (exponent).
• No ()’s in the equations to solve – we’ll deal with those in another program.
• Don’t worry about negative numbers as input either (not yet anyway).
• Using the order of operations (aka: PEMDAS), output the correct result. 
"""
# Assisted with Grok

# math symbols allowed
Math_Symbols = {'+', '-', '*', '/', '^'}

def IsValidString(input_String: str):
    
    
    # Checks to see all chars are valid
    has_a_valid_symbol = all(
    not char.isalpha() or 
    char.isdigit() or 
    char in Math_Symbols or 
    not char.isspace()
    for char in input_String)
    
    # Checks for adjacent symbols
    adjacent_validity = True
    for i in range(len(input_String) - 1):
        if (input_String[i] in Math_Symbols and 
            input_String[i + 1] in Math_Symbols):
            adjacent_validity = False
            break
    
    starts_with_symbol = input_String[0] in Math_Symbols
    ends_with_symbol = input_String[len(input_String) - 1] in Math_Symbols
    either_end_is_symbol = starts_with_symbol or ends_with_symbol
    
    return has_a_valid_symbol and adjacent_validity and not either_end_is_symbol

def Main():
    print("5 FUnction Calculator")
    UserInput = input("Input math, EX: 5+5").strip
    
    operation_m: set[str] = {}
    if IsValidString(UserInput):
        for i in UserInput:
            operation_m.add(i)
    
    for i in operation_m:
        if i in Math_Symbols:
            
    

if __name__ == "__main__":
    Main()