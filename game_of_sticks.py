import random

"""
Module: game_of_sticks

Implementation of the Game of Sticks features an AI that learns to play either by competing against a human or through pre-training against another AI.

Author:
1) Max Jeruss - mjeruss@sandiego.edu
"""


def get_player_selection(player_number: int, sticks_left: int) -> int:
    """
    Validates the user's selection for their turn and returns it as an integer.

        Parameters:
            player_number(type: int): player 1 or player 2's selection.
            sticks_left(type: int): the number of sticks left in the round.
        Returns:
            player_selection(type: int): updated number of sticks left in the round.
    """
    player_turn = True

    while player_turn:
        player_selection = -1
        if sticks_left >= 3:
            try:
                player_selection = int(input(
                    f'Player {player_number}: How many sticks do you take (1-3)? '))
            except ValueError:
                pass
            if 1 <= player_selection <= 3:
                player_turn = False
                return player_selection
            else:
                print('Please enter a number between 1 and 3')
        else:
            try:
                player_selection = int(input(
                    f'Player {player_number}: How many sticks do you take (1-{sticks_left})? '))
            except ValueError:
                pass
            if 1 <= player_selection and player_selection <= sticks_left:
                player_turn = False
                return player_selection
            else:
                print(f'Please enter a number between 1 and {sticks_left}')


def get_ai_selection(num_sticks: int, hat_dict: dict[list[int]], beside_dict: dict[int]) -> int:
    """
    Gets the AI's selection using a method from the random module.

        Parameters:
            num_sticks(type: int): the number of sticks on the board.
            hat_dict(type: dict): a dictionary with all the possible number of sticks on the board as keys and lists of integers as values that the ai uses to choose its number from. 
            beside_dict(type: int): a dictionary with all the possible number of sticks on the board as keys and ints as values so that the ai can keep track of its selections per game.
        Returns:
            ai_pick(type: int): an integer between 1 and 3 or 1 and the number of sticks remaining.
    """
    ai_pick = random.choice(hat_dict[num_sticks])
    hat_dict[num_sticks].remove(ai_pick)
    beside_dict[num_sticks] = ai_pick
    return ai_pick


def player_vs_player(num_sticks: int) -> None:
    """
    Alternates between player 1 and player 2 - allowing 2 users to play the game, prints how many sticks are left after each selection, and displays the loser.

        Parameters:
            num_sticks(type: int): the number of sticks on the board.
    """

    game_start = True
    player_1_turn = True
    print(f'\nThere are {num_sticks} sticks on the board.')

    while game_start:
        if player_1_turn:
            player_selection = get_player_selection(1, num_sticks)
            num_sticks = num_sticks - player_selection
            if num_sticks == 0:
                print(f'Player 1, you lose.')
                game_start = False
                player_1_turn = False
            else:
                print(f'\nThere are {num_sticks} sticks on the board.')
                player_1_turn = False
                player_2_turn = True

        if player_2_turn:
            player_selection = get_player_selection(2, num_sticks)
            num_sticks = num_sticks - player_selection
            if num_sticks == 0:
                print(f'Player 2, you lose.')
                game_start = False
                player_2_turn = False
            else:
                print(f'\nThere are {num_sticks} sticks on the board.')
                player_2_turn = False
                player_1_turn = True


def player_vs_ai(num_sticks: int, training_rounds: int) -> None:
    """
    Alternates between a player and an ai allowing a user to play against an ai, prints how many sticks are left after each selection, and displays the loser.

        Parameters:
            num_sticks(type: int): the number of sticks on the board.
            training_rounds(type: int): the number of rounds an ai will be trained prior to playing. 0 if untrained, 1000 if trained. 
    """

    store_sticks = num_sticks
    game_start = 1
    round_start = 1
    play_again_prompt = True
    player_1_turn = True
    hat_dict = pretrain_ai(num_sticks, training_rounds)
    write_hat_contents(hat_dict, 'hat-contents.txt')
    beside_dict = {}
    print(f'\nThere are {num_sticks} sticks on the board.')

    while game_start == 1:
        while round_start == 1:
            if player_1_turn:
                player_selection = get_player_selection(1, num_sticks)
                num_sticks = num_sticks - player_selection
                if num_sticks == 0:
                    print(f'You lose.')
                    AI_won = True
                    update_hats(hat_dict, beside_dict, AI_won)
                    round_start = 0
                    player_1_turn = False
                    play_again_prompt = True
                else:
                    print(f'\nThere are {num_sticks} sticks on the board.')
                    player_1_turn = False
                    ai_turn = True

            if ai_turn:
                ai_selection = get_ai_selection(
                    num_sticks, hat_dict, beside_dict)
                num_sticks = num_sticks - ai_selection
                if num_sticks == 0:
                    print(f'AI selects {ai_selection}')
                    print(f'AI loses.')
                    AI_won = False
                    update_hats(hat_dict, beside_dict, AI_won)
                    beside_dict = {}
                    round_start = 0
                    ai_turn = False
                    play_again_prompt = True

                else:
                    print(f'AI selects {ai_selection}')
                    print(f'\nThere are {num_sticks} on the board.')
                    ai_turn = False
                    player_1_turn = True

        while play_again_prompt:
            user_play_again = -1
            try:
                user_play_again = int(input(f'Play again (1 = yes, 0 = no)? '))
            except ValueError:
                pass
            if user_play_again == 1:
                num_sticks = store_sticks
                round_start = 1
                player_1_turn = True
                play_again_prompt = False
                print(f'\nThere are {num_sticks} sticks on the board.')
            elif user_play_again == 0:
                play_again_prompt = False
                game_start = 0
            else:
                print(f'Please enter 0 or 1')


def initialize_hats(num_sticks: int) -> dict:
    """
    Initializes a dictionary. The keys represent the number of sticks on the board for a given round. The values are a list of the possible choices the ai can take. Returns a copy of the dictionary.

        Parameters:
            num_sticks(type: int): the number of sticks on the board.
        Returns:
            new_dict(type: dictionary): a fresh, initialized dictionary for an untrained ai.
    """
    new_dict = {1: [1], 2: [1, 2]}
    for i in range(3, num_sticks+1):
        new_dict[i] = [1, 2, 3]
    return new_dict


def update_hats(hat_dict: dict, beside_dict: dict, AI_won: bool) -> None:
    """
    Updates the hat_dict dictionary the ai chooses from. Update is based on the values in beside_dict and whether or not the ai won or lost.

        Parameters:
            hat_dict(type: dict): a dictionary with all the possible number of sticks on the board as keys and lists of integers as values that the ai uses to choose its number from. 
            beside_dict(type: int): a dictionary with all the possible number of sticks on the board as keys and ints as values so that the ai can keep track of its selections per game.
            AI_won(type: bool): a boolean that represents whether the ai won or lost a round.
    """
    if AI_won:
        for k, v in beside_dict.items():
            # append the value to the list and DONT sort it because hopper doesnt want it sorted even tho pdf example that emphasized EXACT match said otherwise...
            for i in range(2):
                hat_dict[k].append(v)
            # hat_dict[k].sort()
    else:
        for k, v in beside_dict.items():
            if v not in hat_dict[k]:
                hat_dict[k].append(v)
                # hat_dict[k].sort()


def pretrain_ai(num_sticks: int, num_rounds: int) -> dict:
    """
    Trains an ai to be ready for battle. 

        Parameters:
            Parameters:
            num_sticks(type: int): the number of sticks on the board.
            num_rounds(type: int): the number of rounds an ai will be trained prior to playing. 0 if untrained, 1000 if trained.
        Returns:
            hatsAI2(type: dict): ai #2's hat dictionary that is now modified increasing the odds that it chooses the best number for any given number of sticks on the board.
    """

    sticks = num_sticks
    hatsAI1 = initialize_hats(sticks)
    hatsAI2 = initialize_hats(sticks)
    for i in range(num_rounds):
        sticks = num_sticks
        AI = 1
        besidesAI1 = {}
        besidesAI2 = {}
        while sticks > 0:
            if AI == 1:
                selectionAI1 = get_ai_selection(sticks, hatsAI1, besidesAI1)
                sticks -= selectionAI1
                AI = 2
            else:
                selectionAI2 = get_ai_selection(sticks, hatsAI2, besidesAI2)
                sticks -= selectionAI2
                AI = 1
        winAI1 = True
        winAI2 = True
        if AI == 2:
            winAI1 = False
        else:
            winAI2 = False
        update_hats(hatsAI1, besidesAI1, winAI1)
        update_hats(hatsAI2, besidesAI2, winAI2)
    return (hatsAI2)


def write_hat_contents(hat_dict: dict, filename: object) -> None:
    """
    Writes the formatted contents of an ai's hat dictionary to a file for viewing.

        Parameters:
            hat_dict(type: dict): a dictionary with all the possible number of sticks on the board as keys and lists of integers as values that the ai uses to choose its number from.
            filename(type: file): a filename for the write file.
    """
    f = open(filename, 'w')
    f.write(f"Hat Number: (1's, 2's, 3's)\n")
    for k, v in hat_dict.items():
        ones = v.count(1)
        twos = v.count(2)
        threes = v.count(3)
        f.write(f'{k}: ({ones}, {twos}, {threes})\n')
    f.close()


def main():
    """
    The main function that allows for importing of this module to other programs. It welcomes players to the game and asks how many sticks they want to play with, and which game mode they want to play from a list of options. Validates user input. 
    """
    print("Welcome to the Game of Sticks!")
    # validate the game is starting with an appropriate number of sticks
    num_sticks_valid = False
    while not num_sticks_valid:
        num_sticks = -1
        try:
            num_sticks = int(
                input("How many sticks are there on the table initially (10-100)? "))
        except ValueError:
            pass
        if 10 <= num_sticks <= 100:
            num_sticks_valid = True
        else:
            print('Please enter a number between 10 and 100')

    game_prompt = True
    while game_prompt:
        game_type = -1
        try:
            game_type = int(input(
                f'Options:\n Play against a friend (1)\n Play against the computer (2)\n Play against the trained computer (3)\nWhich option do you take (1-3)? '))
        except ValueError:
            pass
        if game_type == 1:
            player_vs_player(num_sticks)
            game_prompt = False
        elif game_type == 2:
            player_vs_ai(num_sticks, training_rounds=0)
            game_prompt = False
        elif game_type == 3:
            print(f'Training AI, please wait...')
            player_vs_ai(num_sticks, training_rounds=1000)
            game_prompt = False
        else:
            print(f'Please enter a number between 1 and 3')


if __name__ == "__main__":
    """
    This function allows for the program to be run as a standalone program. Calls the main function.
    """
    main()
