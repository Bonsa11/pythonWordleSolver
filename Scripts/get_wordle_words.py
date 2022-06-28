from Scripts.functions import *


def recommend_word(poss_words, red_set, green_set, yellow_set):
    alphabet = build_alphabet_dict()

    for word in poss_words:
        for letter in word:
            alphabet[letter] += 1

    return alphabet


def find_possible_words(poss_words, red_set, green_set, yellow_set):
    for letter, _ in green_set.items():
        if letter in red_set:
            red_set.remove(letter)

    for letter, _ in yellow_set.items():
        if letter in red_set:
            red_set.remove(letter)

    poss_words = red_set_check(poss_words, red_set)
    poss_words = green_set_check(poss_words, green_set)
    poss_words = yellow_set_check(poss_words, yellow_set)

    print(f'There is {len(poss_words)} possible words still remaining')

    alphabet = recommend_word(poss_words, red_set, green_set, yellow_set)
    remaining_letters = sorted(alphabet.items(), key=lambda x: (-x[1], x[0]))

    scores = get_scores(poss_words, alphabet)

    print(f'the highest scoring words are {scores[:4]}')

    return poss_words
