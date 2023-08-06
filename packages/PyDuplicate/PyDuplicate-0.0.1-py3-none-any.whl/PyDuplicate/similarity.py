"""
This module implements the main functionalities of PyDuplicate.

Author: Jean Bertin
Github: https://github.com/JeanBertinR
"""

__author__ = "Jean Bertin"
__email__ = "jeanbertin.ensam@gmail.com"
__status__ = "planning"

import re
import difflib
from fuzzywuzzy import fuzz
import numpy as np


class SimilarityScorer:
    def __init__(self):
        pass

    def similarity_score(self, str_tuple_1: str, str_tuple_2: str) -> float:
        # Initialize variables
        match_found = False
        total_distance_avg = 0

        # Iterate over corresponding phrases in both tuples
        for phrase1, phrase2 in zip(str_tuple_1, str_tuple_2):
            # Split phrases into words
            words1 = re.split(r"\s+|-", phrase1)
            words2 = re.split(r"\s+|-", phrase2)

            # Iterate over corresponding words in both phrases
            for word1, word2 in zip(words1, words2):
                if word1 != word2:
                    # Check for various conditions to determine if there is a match
                    if (
                            set([word.lower() for word in set(words1)]) == set(
                        [word.lower() for word in set(words2)]) or
                            (
                                    (word2.isalpha() and any(c.islower() for c in word2) and fuzz.ratio(word1,
                                                                                                        word2) / 100 > 0.5) or
                                    word1.lower() == word2.lower()
                            )
                    ):
                        total_distance_avg = 1
                    else:
                        total_distance_avg = 0.5
                        break

            # If a match is found, exit the loop
            if total_distance_avg == 1:
                match_found = True
                break

        # If no match is found, calculate average distances for digits and strings
        if not match_found:
            numbers_in_str_tuple_1 = [re.findall(r'\d+', item) for item in str_tuple_1]
            numbers_in_str_tuple_2 = [re.findall(r'\d+', item) for item in str_tuple_2]
            item_digit_distance = [float(difflib.SequenceMatcher(None, item[0], item[1]).ratio()) for item in
                                   zip(numbers_in_str_tuple_1, numbers_in_str_tuple_2)]
            item_string_distance = [fuzz.ratio(item[0], item[1]) / 100 for item in
                                    zip(list(str_tuple_1), list(str_tuple_2))]
            digit_distance_avg = np.mean(item_digit_distance)
            string_distance_avg = np.mean(item_string_distance)
            total_distance_avg = (
                                             3 * digit_distance_avg + string_distance_avg) / 4  # Give more importance to modified digits than to character strings

        return total_distance_avg