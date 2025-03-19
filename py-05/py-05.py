

""" 
• The user is allowed to use the following operators: +, -, *, /, ^ (exponent).
• No ()’s in the equations to solve – we’ll deal with those in another program.
• Don’t worry about negative numbers as input either (not yet anyway).
• Using the order of operations (aka: PEMDAS), output the correct result. 
"""
# Assisted with Grok (also AI only assisted in making it look nicer, I had to do all the thinking)

# math symbols allowed
Math_Symbols = {'+', '-', '*', '/', '^'}

def IsValidString(input_string: str) -> bool:
    # Allowed characters: digits and math symbols only
    allowed = set("0123456789") | Math_Symbols
    all_chars_valid = all(char in allowed for char in input_string)
    
    # Check for adjacent symbols
    adjacent_validity = True
    for i in range(len(input_string) - 1):
        if input_string[i] in Math_Symbols and input_string[i + 1] in Math_Symbols:
            adjacent_validity = False
            break
    
    # Check if starts or ends with a symbol
    if not input_string:  # Handle empty string
        return False
    starts_with_symbol = input_string[0] in Math_Symbols
    ends_with_symbol = input_string[-1] in Math_Symbols
    either_end_is_symbol = starts_with_symbol or ends_with_symbol
    
    return all_chars_valid and adjacent_validity and not either_end_is_symbol

def tokenize(input_string: str) -> list[str]:
    tokens = []
    current_num = ""
    for char in input_string:
        if char in Math_Symbols:
            if current_num:
                tokens.append(current_num)
                current_num = ""
            tokens.append(char)
        else:
            current_num += char
    if current_num:
        tokens.append(current_num)
    return tokens


def Main():
    while True:
        print("5 FUnction Calculator")
        UserInput = str(input("Input math, EX: 5+5: ").strip())
        
        if UserInput.lower == "exit":
            print("Exiting")
            break
        
        if not IsValidString(UserInput):
            print("Invalid input! Use only digits and +, -, *, /, ^ with no adjacent operators or leading/trailing operators.")
            continue
        
        operation_m = tokenize(UserInput)  # Tokenize correctly
        print(f"Initial operation_m: {operation_m}")
        
        while any(char in Math_Symbols for char in operation_m):  # Process while operators remain
            if '^' in operation_m:
                index = operation_m.index('^')
                value_A, value_B = float(operation_m[index - 1]), float(operation_m[index + 1])
                final_Value = value_A ** value_B
                operation_m[index - 1:index + 2] = [str(final_Value)]
                print(f"After '^' operation: {operation_m}")
                continue
            if '/' in operation_m:
                index = operation_m.index('/')
                value_A, value_B = float(operation_m[index - 1]), float(operation_m[index + 1])
                if value_B == 0:
                    print("Error: Division by zero!")
                    break
                final_Value = value_A / value_B
                operation_m[index - 1:index + 2] = [str(final_Value)]
                print(f"After '/' operation: {operation_m}")
                continue
            if '*' in operation_m:
                index = operation_m.index('*')
                value_A, value_B = float(operation_m[index - 1]), float(operation_m[index + 1])
                final_Value = value_A * value_B
                operation_m[index - 1:index + 2] = [str(final_Value)]
                print(f"After '*' operation: {operation_m}")
                continue
            if '-' in operation_m:
                index = operation_m.index('-')
                value_A, value_B = float(operation_m[index - 1]), float(operation_m[index + 1])
                final_Value = value_A - value_B
                operation_m[index - 1:index + 2] = [str(final_Value)]
                print(f"After '-' operation: {operation_m}")
                continue
            if '+' in operation_m:
                index = operation_m.index('+')
                value_A, value_B = float(operation_m[index - 1]), float(operation_m[index + 1])
                final_Value = value_A + value_B
                operation_m[index - 1:index + 2] = [str(final_Value)]
                print(f"After '+' operation: {operation_m}")
                continue
            break  # Safety exit incase catches fire
        print(f"Final result: {operation_m[0]}")
if __name__ == "__main__":
    Main()