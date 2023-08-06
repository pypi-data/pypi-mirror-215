""" 
Functions that prepare a grid of letters to be printed on the terminal. New rows are 
added when the current row size is greater than the terminal width.
"""
import os
from typing import List


def store_sentence(words: List[str], letter_representation: dict[str, list[list[str]]]):
    terminal_width = os.get_terminal_size().columns
    sentence = []
    word_group = []
    current_width = 0
    for word in words:
        word_representation = []
        word_width = 0
        for letter in word:
            single_letter_representation = letter_representation[letter.upper()]
            word_representation.append(single_letter_representation)
            letter_width = (
                max(len("".join(line)) for line in single_letter_representation) + 1
            )
            word_width += letter_width
        if current_width + word_width + len(word_group) * 4 > terminal_width:
            sentence.append(word_group)
            word_group = [word_representation]
            current_width = word_width
        else:
            word_group.append(word_representation)
            current_width += word_width
    if word_group:
        sentence.append(word_group)
    return sentence


def print_sentence(word_group):
    for i in range(5):
        for word_representation in word_group:
            for letter_representation in word_representation:
                printed_string = "".join(letter_representation[i])
                print("\033[33m" + printed_string, end="")
            print("    ", end="")
        print()
