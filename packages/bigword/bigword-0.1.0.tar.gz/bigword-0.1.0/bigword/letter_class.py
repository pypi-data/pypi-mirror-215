""" 
Class for storing the letter dictionary. As well as applying formatting to the letters.
"""
from .letter_dict import letter_dict


class Letter:
    def __init__(self, spacing: int = 1):
        self.spacing = spacing
        self.letter_representation = letter_dict

    def set_spacing(self):
        """Set the spacing between letters in words"""
        self.letter_representation = {
            key: list(map(lambda row: row + [" "] * self.spacing, value))
            for key, value in self.letter_representation.items()
        }

    def get_letter_representation(self):
        return self.letter_representation
