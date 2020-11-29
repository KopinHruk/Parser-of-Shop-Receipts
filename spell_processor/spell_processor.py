# Module to correct wrong-parsed words.

from spellchecker import SpellChecker
import os
import numpy as np


# spell = SpellChecker()
# spell.word_frequency.load_text_file('ru_full.txt')
#
# # TODO dynamic dictionary for goods
#
# # find those words that may be misspelled
# misspelled = spell.unknown(['СПОЙКА', 'БАБЧШКИН', 'пфжилой', 'ВАОЛИ'])
#
# for word in misspelled:
#     # Get the one `most likely` answer
#     print(spell.correction(word))
#
#     # Get a list of `likely` options
#     print(spell.candidates(word))
#
# print(spell.correction('СПОЙКА'))


class SpellProcessor:
    def __init__(self, first_level_dict='dictionaries/ru_full.txt', second_level_dict='dictionaries/products.txt'):
        # First level
        self.first_level_dict = first_level_dict
        self.spell_checker = SpellChecker()
        self.spell_checker.word_frequency.load_text_file(self.first_level_dict)

        # Second level
        self.second_level_dict = second_level_dict
        self.word_corrector = SpellChecker()

        if not os.path.exists(second_level_dict):
            with open(second_level_dict, 'w'): pass
        self.word_corrector.word_frequency.load_text_file(self.second_level_dict)


    def write_to_dict(self, correct_words):
        with open(self.second_level_dict, "a") as second_dict_file:
            for word in correct_words:
                second_dict_file.write(word + " 1" + "\n")


    def correct(self, products):
        correct_words = []  # This word will be saved to products dictionary
        result_list = []

        for product in products:

            words = product.split(' ')
            fixed_words = []
            for word in words:
                if len(word) > 2 and len(self.word_corrector.known([word])) == 0 and len(self.spell_checker.known([word])) == 1:
                    correct_words.append(word)

                fixed_words.append(self.word_corrector.correction(word))

            result_list.append(' '.join(fixed_words))

        correct_words = np.unique(np.array(correct_words))
        self.write_to_dict(correct_words)
        return result_list