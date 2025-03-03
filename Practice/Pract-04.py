""" Program 1:
Have the user enter a word then output if that word is a palindrome. A word is a palindrome if it
is the same when read forwards and backwards. For example, kayak is a palindrome, computer
is not.
"""

while True:
    try:
        Palindrome: str = str(input("Input a Palindrome: "))
        ReversePalin: str = Palindrome[::-1]
        if Palindrome == ReversePalin:
            break
    except ValueError:
        print("Invalid input. Please enter an integer.")
print(f"{Palindrome} is a Palindrome, the reverse {ReversePalin}")


"""
Program 2:
Anagrams are words that are the same length and contain the same letters, but the letters are in
different orders. For example, “army” and “mary” are anagrams. Write a program that asks the
user for a word then displays all possible anagrams.
Program 3:
Ask the user for their full name, then output their initials. Do this without using split.
Program 4:
Ask the user to enter a complete sentence, including punctuation. Display the sentence one
word at a time, all in uppercase, and without punctuation.
Program 5:
Program 1 had you determine if a word is a palindrome, but phrases can also be palindromes.
Examples include: “taco cat”, “ Was it a cat I saw?”, and “Madam, I'm Adam.” Write a program
that determines if a user-entered phrase is a palindrome. Remember, the input could include
spaces and punctuation, neither of which counts for determining if a phrase is a palindrome.
 """
 
 