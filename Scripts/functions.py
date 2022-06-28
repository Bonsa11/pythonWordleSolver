from nltk.corpus import words


def limit_word_list():
    """
    Find all 5 letter words in the NLTK dictionary

    :return all_wordle_worlds: list of all possible worlds in wordle
    """

    return list({x.lower() for x in words.words() if len(x) == 5})


def red_set_check(poss_words, red_set):
    still_poss_words = poss_words.copy()

    for letter in red_set:
        # print(f'searching for words without the letter {letter}')
        for word in poss_words:
            if letter in word and word in still_poss_words:
                still_poss_words.remove(word)
    return still_poss_words


def green_set_check(poss_words, green_set):
    still_poss_words = poss_words.copy()

    if len(green_set) == 0:
        return poss_words

    for letter, positions in green_set.items():
            # print(f'searching for words with the letter {letter} in positions {positions}')
        for position in positions:
            for word in poss_words:
                if letter not in word[position]:
                    try:
                        still_poss_words.remove(word)
                    except Exception as e:
                        pass
    return still_poss_words


def yellow_set_check(poss_words, yellow_set):
    still_poss_words = poss_words.copy()

    if len(yellow_set) == 0:
        return poss_words

    for letter, positions in yellow_set.items():
        # print(f'searching for for words without the letter {letter} in positions {positions}')
        for position in positions:
            for word in poss_words:
                if (
                    letter in word
                    and letter in word[position]
                    or letter not in word
                ):
                    try:
                        still_poss_words.remove(word)
                    except Exception as e:
                        pass
    return still_poss_words


def build_alphabet_dict():
    return {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0,
        'h': 0,
        'i': 0,
        'j': 0,
        'k': 0,
        'l': 0,
        'm': 0,
        'n': 0,
        'o': 0,
        'p': 0,
        'q': 0,
        'r': 0,
        's': 0,
        't': 0,
        'u': 0,
        'v': 0,
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }


def words_with(poss_words, letters):
    list_of_letters = [x[0] for x in letters]
    all_letters = []
    some_letters = []
    for word in poss_words:
        count = sum(letter in word for letter in list_of_letters)
        if count == 5:
            all_letters.append(word)

        if count > 2:
            some_letters.append(word)

    return all_letters, some_letters


def get_scores(poss_words, alphabet):
    word_scores = {}

    for word in poss_words:
        score = 0
        letters = []
        for letter in word:
            if letter not in letters:
                letters.append(letter)
                score += alphabet[letter]
            elif len(poss_words) < 100:
                score += alphabet[letter]
        word_scores[word] = score

    return sorted(word_scores.items(), key=lambda x: (-x[1], x[0]))
