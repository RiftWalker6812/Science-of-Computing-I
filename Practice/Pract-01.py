# Program 1
""" Ask the user for a number and output the square of that number. E.g., input = 7, output = 49
"""
def prog1():
    x = int(input('input a number and ill give you a square of that number: '))
    print(x * x)
    
"""
Program 2:
Write a program that asks the user for two angles in a triangle then outputs what the third
measures. (Remember, the three angles in a triangle add to 180 degrees.)
If the two input angles add to 180 or more, output an error message. """
def prog2():
    print('input 2 angles that will add up to a 180 degrees in a triangle')
    triag1 = int(input('Triangle 1: '))
    triage2 = int(input('Triangle 2: '))
    if triag1 + triage2 == 180:
        print('the values you have added add up to 180, this isnt a triangle :(\ntry again')
        prog2()
    else: 
        print(f'the third triangle is {180 - (triag1 + triage2)}')
     
"""   
Program 3:
Ask the user for a number, then tell them if that number is even or odd. (HINT: One of the
operators will make this easy for you!) """
def prog3():
    num = int(input("Enter a number: "))
    if num % 2 is 0:
        print(f"{num} is even.")
    else:
        print(f"{num} is odd.")

"""
Program 4:
Ask the user for two numbers. Then do “little kid division” (where you divide AND show the
remainder  no decimals!!!) and output the result.
Example: 17 divided by 5 is 3 R 2 (R = remainder) """
def prog4():
    print('you will give me two numbers and this will divide and also give remainder')
    x = int(input('first integer: '))
    y = int(input('second integer'))
    remainder = x % y
    print(f'The quotient is: {x//y}, and the remainder is: {x%y}')

"""
Program 5:
Ask the user for a multi-digit number then output the most significant digit. (Be sure to test this
one with 4+ digits!)
Example: The most significant digit of 456987 is 4."""
def prog5():
    i = str(input('input the a multi digit number and this will give the significant digit: '))
    print(f'the significant digit is: {i[0]}')
"""
Program 6:
Write a program that will determine if a year is a leap year. Not that I have put in suggestions for
where to stop and test what you have before moving on.
1. Get correct input:
a. Ask the user for a year.
b. If the user inputs a year before 1582, output an error message. (Test!)
2. Determine if it’s a leap year: (Test after each step!)
a. A leap year happens if the year is divisible by 4. (Test!)
b. Unless it’s also divisible by 100. (Test!)
c. But not 400. (Test!)
For example: 2004 is a leap year, 1900 is not, 2000 is, and 2022 is not.
3. LAST: Put it all inside of a loop so the program keeps asking until the user enters 0    """
def prog6(): 
    is_divisible = lambda a, b: a % b is 0 
    year = int(input("input 0 if you want to exit\ninput a year and it will determine if its a leap year: "))
    if year is 0:
        exit()
    if (year is 1582 or is_divisible(year, 4) or is_divisible(year, 100) or not is_divisible(year, 400)):
        print("Test!\nTry again!")  
        
def prog7():
    #just chaos :)
    def sub1():
        def average(a, b):
            return (a + b)/2
        vi = int(input("average of 2 numbers\nenter first value int: "))
        vt = int(input("enter second value: "))
        print(f"The average of the {vi} and {vt} is {average(vi, vt)}")
    
    def sub2():
        is_divisible_by_79 = lambda a: a % 79 is 0
        num = int(input("Input a int and will test for divisibility by 79: "))
        if is_divisible_by_79(num):
            print(f"{num} is divisible 79")
        else:
            print(f"{num} is not divisible by 79")
    
    def sub3():
        import math
        n = int(input("Input a int that you want to find the facotial for: "))
        print(f"the factorial of {n} is {math.factorial(n)}")
        
    sub_menu = {
        0: exit,
        1: sub1,
        2: sub2,
        3: sub3
    }
    
    def InvalidOption2():
        print("You have inputed an invalid option!")
        
    user_inp2 = int(input('pick a program to start between 0 and 3: '))
    sub_menu.get(user_inp2, InvalidOption2)()
    prog7()
    
menu_controller = {
    0: exit,
    1: prog1,
    2: prog2,
    3: prog3,
    4: prog4,
    5: prog5,
    6: prog6,
    7: prog7
}
   
#Function call MENU
def main():
    def InvalidOption():
        print("You have inputed an invalid option!")
    user_inp = int(input('pick a program to start between 0 and 7: '))
    menu_controller.get(user_inp, InvalidOption)()
    main()

#Start
main()