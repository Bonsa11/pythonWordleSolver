from Scripts.get_wordle_words import *


# from GUI.keyboard import *

def start_game(word_to_guess):
    red_set = []
    green_set = {}
    yellow_set = {}

    _, guessed_word = find_possible_words(limit_word_list(), red_set, green_set, yellow_set)

    return guessed_word, red_set, yellow_set, green_set


def play_round(word_to_guess, guessed_word, red_set, yellow_set, green_set):
    if guessed_word == word_to_guess:
        print(F'WORD WAS {guessed_word.upper()}')
        return True, red_set, yellow_set, green_set

    else:
        for position, guessed_letter in enumerate(guessed_word):
            #print(position, guessed_letter)
            if guessed_letter not in word_to_guess:
                red_set.append(guessed_letter)
            elif guessed_letter == word_to_guess[position]:
                if guessed_letter not in green_set:
                    green_set[guessed_letter] = [position]
                else:
                    green_set[guessed_letter].append(position)
            else:
                if guessed_letter not in yellow_set:
                    yellow_set[guessed_letter] = [position]
                else:
                    yellow_set[guessed_letter].append(position)

        #print(red_set, '\n', yellow_set, '\n', green_set)
        return False, red_set, yellow_set, green_set


def play_wordle(word_to_guess):
    winner = False
    guessed_word, red_set, yellow_set, green_set = start_game(word_to_guess)
    round = 1
    words = []
    no_of_words = []
    while not winner:
        print(f'THE GUESS FOR ROUND {round} IS {guessed_word.upper()}')
        winner, red_set, yellow_set, green_set = play_round(word_to_guess, guessed_word, red_set, yellow_set, green_set)
        if winner:
            break
        _, guessed_word = find_possible_words(limit_word_list(), red_set, green_set, yellow_set)
        words.append(guessed_word)
        no_of_words.append(len(_))
        round += 1

    return round, words, no_of_words


if __name__ == '__main__':
    word_to_guess = 'count'
    rounds, no_of_words = play_wordle(word_to_guess)
