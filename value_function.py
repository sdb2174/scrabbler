RACK_MAX = 7
FV_WEIGHT_NUM = 26

import random
import os
import numpy as np
import matplotlib.pyplot as plt 

import scrabbler as sc
from scrabbler.dictionary import Dictionary
import utilities.logger as logger

RACK_MAX = 7

LETTER_VALUE = {}
with open("resources/scrabble/tile_list.txt") as f:
    for line in f:
        (key, val) = line.split()
        LETTER_VALUE[key] = int(val)

script_dir = os.path.dirname(__file__)
resource_dir = os.path.join(script_dir, "resources")
resource_directory = os.path.join(resource_dir, "scrabble")
saved_dictionary_path = os.path.join(resource_directory, "dictionary.p")

logger.info("loading saved dictionary file...")
global_dictionary = Dictionary.load_from_pickle(saved_dictionary_path)
bag_o = ["A", "A", "A", "A", "A", "A", "A", "A", "A",
         "B", "B",
         "C", "C",
         "D", "D", "D", "D",
         "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E",
         "F", "F",
         "G", "G", "G",
         "H", "H",
         "I", "I", "I", "I", "I", "I", "I", "I", "I",
         "J",
         "K",
         "L", "L", "L", "L",
         "M", "M",
         "N", "N", "N", "N", "N", "N",
         "O", "O", "O", "O", "O", "O", "O", "O",
         "P", "P",
         "Q",
         "R", "R", "R", "R", "R", "R",
         "S", "S", "S", "S",
         "T", "T", "T", "T", "T", "T",
         "U", "U", "U", "U",
         "V", "V",
         "W", "W",
         "X",
         "Y", "Y",
         "Z"]


STEP_SIZE = 1e-3


# Experimentation with full game play-out from no state.

def main():
    weights = np.random.rand(FV_WEIGHT_NUM, 1)
    diff = []

    for i in range(1500):
        print("iter:",i)
        bag = bag_o.copy()
        random.shuffle(bag)
        score1 = 0  # resetting the scores and bag:
        score2 = 0
        game = sc.Game(filename="/Users/sbrosh1/Documents/GitHub/scrabbler/games/start_state.p",
                                global_dictionary=global_dictionary, enable_logger=False)
        rack1 = []
        rack2 = []
        for i in range(RACK_MAX):
            rack1.append(bag.pop())
            rack2.append(bag.pop())

        moves = game.find_best_moves(rack1, num = 20)
        if moves:
            move = choose_move(moves)
            game.play(move.start_square, move.word, move.direction)
            score1 = score1 + move.score

            rack1 = remove_specific_letters(rack1, move.word)


            # Get feature vector using vectorize function, an approximate the value function.
            approx_vf = np.dot(vectorize(rack1), weights)
                
            # Draw the number of letters played:
            for l in range(len(move.word)):
                rack1.append(bag.pop())

        # If unable to play a move:
        # else:
        #     for l in range(len(rack1)):
        #         if LETTER_VALUE[rack1[l]] > 4:
        #             bag.append(rack1[l])
        #             random.shuffle(bag)
        #             rack1 = rack1.replace(rack1[l], bag.pop(), 1)
            

        moves = game.find_best_moves(rack2, num = 1)
        if moves:
            game.play(moves[0].start_square, moves[0].word, moves[0].direction)
            score2 = score2 + moves[0].score

            rack2 = remove_specific_letters(rack2, moves[0].word)
            for l in range(len(moves[0].word)):
                rack2.append(bag.pop())

            # for i in range(len(moves[0].word)):                    
            #     if len(bag) > 0:
            #         rack2 = rack2.replace(moves[0].word[i], bag.pop(), 1)
            #     else:
            #         rack2 = rack2.replace(moves[0].word[i], '', 1)

        # else:
        #     for l in range(len(rack2)):
        #         if LETTER_VALUE[rack2[l]] > 4:
        #             bag.append(rack2[l])
        #             random.shuffle(bag)
        #             rack2 = rack2.replace(rack2[l], bag.pop(), 1)



        # Now, play the next move, and see what the effect of leaving those above tiles has on the scores:

        moves = game.find_best_moves(rack1, num = 1)
        if moves:
            move = choose_move(moves)
            game.play(move.start_square, move.word, move.direction)
            score1 = score1 + move.score
            term1 = move.score
            rack1 = remove_specific_letters(rack1, move.word)
            # Draw the number of letters played:
            for l in range(len(move.word)):
                rack1.append(bag.pop())
            # for i in range(len(moves[0].word)):                    
            #     if len(bag) > 0:
            #         rack1 = rack1.replace(moves[0].word[i], bag.pop(), 1)
            #     else:
            #         rack1 = rack1.replace(moves[0].word[i], '', 1)

        # If unable to play a move:
        else:
            for l in range(len(rack1)):
                if LETTER_VALUE[rack1[l]] > 4:
                    bag.append(rack1[l])
                    random.shuffle(bag)
                    rack1 = rack1.replace(rack1[l], bag.pop(), 1)


        # Player 2 plays:
        moves = game.find_best_moves(rack2, num = 0)
        if moves:
            game.play(moves[0].start_square, moves[0].word, moves[0].direction)
            score2 = score2 + moves[0].score
            term2 = moves[0].score 
            rack2 = remove_specific_letters(rack2, moves[0].word)
            for l in range(len(moves[0].word)):
                rack2.append(bag.pop())

            # for i in range(len(moves[0].word)):                    
            #     if len(bag) > 0:
            #         rack2 = rack2.replace(moves[0].word[i], bag.pop(), 1)
            #     else:
            #         rack2 = rack2.replace(moves[0].word[i], '', 1)

        else:
            for l in range(len(rack2)):
                if LETTER_VALUE[rack2[l]] > 4:
                    bag.append(rack2[l])
                    random.shuffle(bag)
                    rack2 = rack2.replace(rack2[l], bag.pop(), 1)


        # Now, we need to calculate the true value function:
        # We do this by subtracting the scores from the second play above.
        # By computing the evaluation function this way, the aim is to see if there is a pattern between leaving certain letters, 
        # and scoring a higher score in the next move.
        true_vf = term1


        diff.append(true_vf - approx_vf)
        
        delw = STEP_SIZE * (true_vf - approx_vf) * weights 
        weights = weights + delw # Not experiencing exploding or vanishing gradients after 1500 iterations.

        print(true_vf - approx_vf)
    
    # np.save(weights)
    print(weights)

    # Compute the moving average with window length 50
    window_length = 50
    moving_average = np.convolve(diff, np.ones(window_length)/window_length, mode='valid')

    plt.plot(moving_average)
    plt.show()


def vectorize( rack):
    # First, place the (simplified) board state into the feature vector:
    # vec = []
    # for i in range(15):
    #     for j in range(15):
    #         if board.square(i, j)._tile:
    #             vec.append(ord(board.square(i, j)._tile))
    #             print(ord((board.square(i, j)._tile)))
    #         else:
    #             vec.append(0)
    # Next, place the entirety of the rack into the feature vector:
    # for i in range(RACK_MAX):
    #     vec.append(ord(rack[i]))

    # vec.append(score1)
    # vec.append(score2)
    # return vec
    vectorized_leave = [0]*26 # Our vectorized version of the leaves which we will update to represent the leaves below
    for letter in rack:
        index = ord(letter) - 65
        vectorized_leave[index] += 1

    return vectorized_leave 


def encode(board, rack, move):
    rows, cols, n = (15, 15, 28)
    vec = [[[0 for k in range(cols)] for j in range(rows)] for i in range(n)]



    for i in range(rows):
        for j in range(cols):
            if board.square(i, j)._tile:
                vec[i][j][0] = 1
                vec[i][j][ord(board.square(i, j)._tile) - 96 + 1] = 1
                
            else:
                vec[i][j][0] = 0
                vec[i][j][1] = 0



def choose_move(moves, game=None, bag=None, played=None):
    # start by running an episode for the first move:
    eps = 0.75
    r = random.uniform(0, 1)
    if r <= eps:
        move = random.choice(moves)
    else:
        # the parameterized policy will select the move, given the state (board, bag, played, etc.)
        move = moves[0]

    return move

def remove_specific_letters(arr, letters_to_remove):
    return [string for string in arr if not any(letter in string for letter in letters_to_remove)]



if __name__ == "__main__":
    main()
