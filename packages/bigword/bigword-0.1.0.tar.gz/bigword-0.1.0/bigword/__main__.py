""" 
Main file for the Bigword package.
"""
import argparse
import sys
import logging

from .grid import print_sentence, store_sentence
from .letter_class import Letter


def bigword():
    parser = argparse.ArgumentParser(description="Print words on a grid")

    parser.add_argument(
        "words",
        type=str,
        nargs="?",
        help="The sentence to print. Must pass in as a continuous string.\nExample: bigwords 'this is a bigg ol sentence'",
    )

    args = parser.parse_args()

    if args.words is None:
        logging.error("Please pass in a sentence to print")
        sys.exit(1)

    elif not isinstance(args.words, str):
        logging.error("Argument must be a string")
        sys.exit(1)

    l = Letter()
    l.set_spacing()
    letter_representation = l.get_letter_representation()

    words = args.words.split()

    sentence = store_sentence(words, letter_representation)
    for word_group in sentence:
        print_sentence(word_group)
        print()


if __name__ == "__main__":
    bigword()
