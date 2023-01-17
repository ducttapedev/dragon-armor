from __future__ import print_function

# Words that are always interpreted as numbers regardless of context
ANYWHERE_NUMERICAL_WORDS = {
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
}

# Words that should be typed out as a complete word if they are on their own,
# but should be converted into a number if they are a part of a larger numeric word
NON_SINGLE_NUMERIC_WORDS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

# Words that can be a part of a number, but not the first word
NONSTARTER_NUMERICAL_WORDS = {
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'point': '.'
}

NONSTARTER_NUMERICAL_JOINING_WORDS = [
    'and',
]

ALL_NUMERIC_WORDS = {
    **ANYWHERE_NUMERICAL_WORDS,
    **NON_SINGLE_NUMERIC_WORDS,
    **NONSTARTER_NUMERICAL_WORDS,
}

decimal_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

"""
#TODO
indian_number_system = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'lac': 100000,
    'lakh': 100000,
    'crore': 10000000
}
"""


def number_formation(number_words):
    """
    function to form numeric multipliers for million, billion, thousand etc.
    Python function documentation before or after function definition
    input: list of strings
    return value: integer
    """
    numbers = []
    for number_word in number_words:
        numbers.append(ALL_NUMERIC_WORDS[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


def get_decimal_sum(decimal_digit_words):
    """
    function to convert post decimal digit words to numerial digits
    input: list of strings
    output: double
    """
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if dec_word not in decimal_words:
            return 0
        else:
            decimal_number_str.append(ALL_NUMERIC_WORDS[dec_word])
    final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
    return float(final_decimal_string)


def mixed_word_to_number(number_sentence):
    """
    Convert a sentence that may contain both regular words and numerical words into
    a sentence that replaces the numerical words with numbers
    """
    if type(number_sentence) is not str:
        raise ValueError(
            "Type of input is not string! Please enter a valid number word"
            " (eg. \'two million twenty three thousand and forty nine\')"
        )

    if number_sentence.isdigit():  # return the number if user enters a number string
        return int(number_sentence)

    split_words = number_sentence.strip().split(" ")  # strip extra spaces and split sentence into words

    number_words = []
    result = []
    for word in split_words:
        # Normalize the word to make it easier to identify if it is numeric
        normalized_word = normalize_word_for_number(word)

        # Words that are always interpreted as numeric
        if normalized_word in ANYWHERE_NUMERICAL_WORDS or normalized_word in NON_SINGLE_NUMERIC_WORDS:
            number_words.append(word)
        # Words that are interpreted as numeric if they are not the first word
        elif number_words and (normalized_word in NONSTARTER_NUMERICAL_WORDS
                               or normalized_word in NONSTARTER_NUMERICAL_JOINING_WORDS):
            number_words.append(word)
        # Words that are not interpreted as numeric
        else:
            # Convert the preceding string of numeric words into numbers, if preceded by such
            if number_words:
                result += maybe_word_to_number(number_words)
                number_words = []
            result.append(word)

    # Convert the last string of numeric words into numbers, if it ends with numeric words
    if number_words:
        result += maybe_word_to_number(number_words)
    return result


def maybe_word_to_number(number_words):
    if not number_words:
        return []
    # Convert the preceding string of numeric words into numbers, if preceded by such
    if len(number_words) == 1 and normalize_word_for_number(number_words[0]) in NON_SINGLE_NUMERIC_WORDS:
        return number_words

    normalized_number_words = [
        normalize_word_for_number(w)
        for w in number_words
        if normalize_word_for_number(w) in ALL_NUMERIC_WORDS
    ]
    return [str(word_to_num(normalized_number_words))]


def normalize_word_for_number(word):
    """
    Normalize the word to make it easier to identify if it is numeric
    """
    return word.lower()


def word_to_num(clean_numbers):
    clean_decimal_numbers = []

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        raise ValueError(
            "No valid number words found! Please enter a valid number word"
            " (eg. two million twenty three thousand and forty nine)")

    # Error if user enters million,billion, thousand or decimal point twice
    if clean_numbers.count('thousand') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count(
            'billion') > 1 or clean_numbers.count('point') > 1:
        raise ValueError(
            "Redundant number word! Please enter a valid number word"
            " (eg. two million twenty three thousand and forty nine)")

    # separate decimal part of number (if exists)
    if clean_numbers.count('point') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('point') + 1:]
        clean_numbers = clean_numbers[:clean_numbers.index('point')]

    billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
    thousand_index = clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (
            -1 < million_index < billion_index):
        raise ValueError(
            "Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    total_sum = 0  # storing the number to be returned

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
            total_sum += ANYWHERE_NUMERICAL_WORDS[clean_numbers[0]]

        else:
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index + 1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index + 1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index + 1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum += thousand_multiplier * 1000

            hundreds = 0
            if thousand_index > -1:
                if thousand_index != len(clean_numbers) - 1:
                    hundreds = number_formation(clean_numbers[thousand_index + 1:])
            elif million_index > -1:
                if million_index != len(clean_numbers) - 1:
                    hundreds = number_formation(clean_numbers[million_index + 1:])
            elif billion_index > -1:
                if billion_index != len(clean_numbers) - 1:
                    hundreds = number_formation(clean_numbers[billion_index + 1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum += hundreds

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_sum(clean_decimal_numbers)
        total_sum += decimal_sum

    return total_sum


if __name__ == '__main__':
    print(mixed_word_to_number("hello two million twenty three thousand and forty nine world"))
    print(mixed_word_to_number("one time I had three days off"))
    print(mixed_word_to_number("testing one two three"))