from Scripts.get_wordle_words import *

red_set = ['i', 'd', 'e', 'u', 'g', 'l']
yellow_set = {'o': [2,3]}
green_set = {'r': [0]}


def main():
    find_possible_words(limit_word_list(), red_set, green_set, yellow_set)


if __name__ == '__main__':
    main()

