
import random

def Gets_A_RANDOM_NUMBER_BETWEEN_THIS_AND_THAT_OVER_THE_WALL_OF_CODE_FALSE_CHAOS(a):
    return random.randint(1, int(a * .5))
def Gets_A_RANDOM_NUMBER_BETWEEN_THIS_AND_THAT_OVER_THE_WALL_OF_CODE_FALSE_CHAOS(a, b):
    return random.randint(a, b)

#The initilizating of the game that both rules use just returns a random and another a choice
def Initilize_Game_of_Nim():
    w = ""
    if random.choice([False, True]):
        w = "AI"
    else:
        w = "Player"
    print(f"{w} will go first")
    p = Gets_A_RANDOM_NUMBER_BETWEEN_THIS_AND_THAT_OVER_THE_WALL_OF_CODE_FALSE_CHAOS(10, 100)
    
    return w, p

#The Game loop for the game, this is the loop for easy and hard
#The way it does this while using 2 rule sets it by turning the
#Functions into variables and shubing it into it.
def game_loop(pri, defi, pile, turn):
    while(True):
        print(pri)
        if turn is "AI":
            print("It is now the AI's turn")
            marbles_taken = defi(pile)
            print(f"AI pulls {marbles_taken}")
            if pile is 0:
                print("Player Has Won the game")
                break
            turn = "Player"
        elif turn is "Player":
            print(f"It is now the players turn, pick a number between 1 and {int(pile * .5)}")
            marbles_taken = int(input("Input take: "))
            print(f"Player take {marbles_taken}")
            if pile is 0:
                print("Player has LOST!")
                break
        else:
            print("ERROR")
            exit()

def Easy_Mode():
    print("Easy Mode Selected")
    who_goes_First, pile = Initilize_Game_of_Nim()
    
    game_loop(f"There are {pile} marbles in the pile", Gets_A_RANDOM_NUMBER_BETWEEN_THIS_AND_THAT_OVER_THE_WALL_OF_CODE_FALSE_CHAOS, pile, who_goes_First)
            
def Hard_Mode():
    def MAKE_IT_HARDER_FOR_THE_PLAYER(pile): #JUST IMAGINE IF I START MAKING ALL OF THE VARIABLES ENIGMATIC
        n = 1
        while True:
            num = (2**n) - 1
            if num >= pile:
                break
            n += 1
        return num    
    
    print("Hard Mode Selected")
    who_The_Turn_IS_IT, pile = Initilize_Game_of_Nim()
    game_loop("HARD MODE DOESNT GIVE YOU A PILE COUNT, WHY YOU ASK, IM IN COMMAND NOW (SCREECHES)!!!  🙂", MAKE_IT_HARDER_FOR_THE_PLAYER, pile, who_The_Turn_IS_IT)

def main():
    print("🚀")
    print("Hello, welcome to the game of Nim\nWould you like to play, please select an option below.\n0) Exit\n1) Easy Mode\n2) Hard Mode")
    
    print("PH MENU OPTIONS")
    
print("Starting...")    
main()  

if __name__ == '__main__':
    main()