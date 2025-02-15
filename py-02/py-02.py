"""
This Python program is a fun and chaotic take on the Game of Nim, where players take turns removing marbles from a pile. 
The goal is to avoid taking the last marble. The game features Easy and Hard modes, 
with the AI using random moves in Easy Mode and a strategic (but slightly unpredictable) approach in Hard Mode. 
It uses Enum for turn management and includes error handling for invalid inputs. 
The randomness adds an unexpected twist, making each game unique and entertaining! 🎮🔥
"""

import random
from enum import Enum

class Turn(Enum):
    PLAYER = "Player",
    AI = "Ai" 

def False_Chaos(a):
    if a is 1:
        return 1
    return random.randint(1, int(a * .5))
# def False_Chaos(a, b):
#    return random.randint(a, b)

#The initilizating of the game that both rules use just returns a random and another a choice
def Initilize_Game_of_Nim():
    turn = Turn.AI if random.choice([False, True]) else Turn.PLAYER
    print(f"{turn} will go first")
    p = random.randint(10, 100)
    return turn, p

#The Game loop for the game, this is the loop for easy and hard
#The way it does this while using 2 rule sets it by turning the
#Functions into variables and shubing it into it.
def game_loop(a, b, c ,d):
    pri, defi, pile, turn = a, b, c, d # This is done so it doesnt reference the old values
    print(pri)
    while(True):
        if turn == Turn.AI:
            print("It is now the AI's turn")
            marbles_taken = defi(pile + random.randint(0, 2)) # Introduced an extra level of chaos so that the ai can overtake
            pile -= marbles_taken
            print(f"AI pulls {marbles_taken} Marbles")
            if pile <= 0:
                print("Player Has Won the game")
                break
            turn = Turn.PLAYER
        elif turn is Turn.PLAYER:
            # Introduced a level of randomess so that the player can accidently overtake
            print(f"It is now the players turn")
            while True:
                try:
                    max_take = max(1, int(pile * 0.5))  # Ensure the minimum take is 1
                    marbles_taken = int(input(f"Input take (1 to {max_take + random.randint(1, 3)}): "))
                    """ if 1 <= marbles_taken <= max_take:
                        break 
                    else:
                        print("Invalid move! Choose a number within the allowed range.")"""
                    break # Why do we need to check for this ^^^?
                except ValueError:
                    print("Invalid input! Enter a valid number.")
            pile -= marbles_taken
            print(f"Player take {marbles_taken} Marbles")
            if pile <= 0:
                print("Player has LOST! (╯‵□′)╯︵┻━┻")
                break
            turn = Turn.AI
        else:
            print("ERROR")
            exit()

#Easy Mode definition for the game loop     
def Easy_Mode():
    print("Easy Mode Selected")
    who_goes_First, pile = Initilize_Game_of_Nim()
    game_loop(f"There are {pile} marbles in the pile", False_Chaos, pile, who_goes_First)

#Hard Mode definition for the game loop            
def Hard_Mode():
    def MAKE_IT_HARDER_FOR_THE_PLAYER(pile):
        power = 1
        while (2**power - 1) <= pile:
            power += 1
        best_move = pile - (2**(power - 1) - 1)
        
        # If best_move is 0 or greater than half of pile, make a random move instead
        if best_move == 0 or best_move > int(pile * 0.5):
            return random.randint(1, int(pile * 0.5))
        return best_move
    
    print("Hard Mode Selected")
    who_The_Turn_IS_IT, pile = Initilize_Game_of_Nim()
    game_loop("The number of marbles in the pile is a mystery 🙂", MAKE_IT_HARDER_FOR_THE_PLAYER, pile, who_The_Turn_IS_IT)

# AN invalid option default case
def InvalidOption():
    print("Invalid selection! Please enter a valid number.")

# MAIN FUNCTION
def main():
    # Options 
    option_Selection = {
        0: exit,
        1: Easy_Mode,
        2: Hard_Mode
    }
    
    print("🚀 Hello, welcome to the game of Nim 🚀")
    # OPTION SELECTION
    while True:
        print("\nWould you like to play? Please select an option below.")
        print("0) Exit\n1) Easy Mode\n2) Hard Mode")
        try:
            user_Input = int(input("Choose an option: "))
            option_Selection.get(user_Input, InvalidOption)()
        except ValueError:
            print("Invalid input! Please enter a number.")

# So that program doesnt catch fire
if __name__ == '__main__':
    main()
