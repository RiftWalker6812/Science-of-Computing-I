
import random

def Easy_Mode():
    who_goes_First = str
    if random.choice(False, True):
        who_goes_First = "AI"
    else:
        who_goes_First = "Player"
    print(f"Easy Mode selected {who_goes_First} will go first")
    pile = random.randint(10, 100)
    
    while(True):
        print(f"There are {pile} marbles in the pile")
        if who_goes_First is "AI":
            print("It is now the AI's turn")
            marbles_taken = random.randint(1, int(pile * .5))
            print(f"AI pulls {marbles_taken}")
            if pile is 0:
                print("Player Has Won the game")
                break
            who_goes_First = "Player"
        elif who_goes_First is "Player":
            print(f"It is now the players turn, pick a number between 1 and {int(pile * .5)}\n")
            marbles_taken = int(input())
            
            

def Hard_Mode():
    print("PH")

def main():
    print("PH")
    print("Hello, welcome to the game of Nim\nWould you like to play, please select an option below.\n0) Exit\n1) Easy Mode\n2) Hard Mode")
    
    
main()  