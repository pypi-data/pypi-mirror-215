from enum import Enum

from openrgb.utils import RGBColor

from . import Instrument
from ..constants import LED_OFF


class Morse(Enum):
    DOT = 1
    DASH = 2
    SPACE = 3


ASCII_UPPERCASE_TO_MORSE = {
    # Letters
    "A": [Morse.DOT, Morse.DASH],
    "B": [Morse.DASH, Morse.DOT, Morse.DOT, Morse.DOT],
    "C": [Morse.DASH, Morse.DOT, Morse.DASH, Morse.DOT],
    "D": [Morse.DASH, Morse.DOT, Morse.DOT],
    "E": [Morse.DOT],
    "F": [Morse.DOT, Morse.DOT, Morse.DASH, Morse.DOT],
    "G": [Morse.DASH, Morse.DASH, Morse.DOT],
    "H": [Morse.DOT, Morse.DOT, Morse.DOT, Morse.DOT],
    "I": [Morse.DOT, Morse.DOT],
    "J": [Morse.DOT, Morse.DASH, Morse.DASH, Morse.DASH],
    "K": [Morse.DASH, Morse.DOT, Morse.DASH],
    "L": [Morse.DOT, Morse.DASH, Morse.DOT, Morse.DOT],
    "M": [Morse.DASH, Morse.DASH],
    "N": [Morse.DASH, Morse.DOT],
    "O": [Morse.DASH, Morse.DASH, Morse.DASH],
    "P": [Morse.DOT, Morse.DASH, Morse.DASH, Morse.DOT],
    "Q": [Morse.DASH, Morse.DASH, Morse.DOT, Morse.DASH],
    "R": [Morse.DOT, Morse.DASH, Morse.DOT],
    "S": [Morse.DOT, Morse.DOT, Morse.DOT],
    "T": [Morse.DASH],
    "U": [Morse.DOT, Morse.DOT, Morse.DASH],
    "V": [Morse.DOT, Morse.DOT, Morse.DOT, Morse.DASH],
    "W": [Morse.DOT, Morse.DASH, Morse.DASH],
    "X": [Morse.DASH, Morse.DOT, Morse.DOT, Morse.DASH],
    "Y": [Morse.DASH, Morse.DOT, Morse.DASH, Morse.DASH],
    "Z": [Morse.DASH, Morse.DASH, Morse.DOT, Morse.DOT],
    # Digits
    "1": [Morse.DOT, Morse.DASH, Morse.DASH, Morse.DASH, Morse.DASH],
    "2": [Morse.DOT, Morse.DOT, Morse.DASH, Morse.DASH, Morse.DASH],
    "3": [Morse.DOT, Morse.DOT, Morse.DOT, Morse.DASH, Morse.DASH],
    "4": [Morse.DOT, Morse.DOT, Morse.DOT, Morse.DOT, Morse.DASH],
    "5": [Morse.DOT, Morse.DOT, Morse.DOT, Morse.DOT, Morse.DOT],
    "6": [Morse.DASH, Morse.DOT, Morse.DOT, Morse.DOT, Morse.DOT],
    "7": [Morse.DASH, Morse.DASH, Morse.DOT, Morse.DOT, Morse.DOT],
    "8": [Morse.DASH, Morse.DASH, Morse.DASH, Morse.DOT, Morse.DOT],
    "9": [Morse.DASH, Morse.DASH, Morse.DASH, Morse.DASH, Morse.DOT],
    "0": [Morse.DASH, Morse.DASH, Morse.DASH, Morse.DASH, Morse.DASH],
    # Special cases
    " ": [Morse.SPACE],
}


class MorseCode(Instrument):
    """Display the given message in Morse code."""

    def __init__(self, message, hex_colour="#FFFFFF"):
        """
        message: The text to display in Morse code. Allowed characters are a-z/A-Z, 0-9, and space.
        hex_colour: The hex colour to use when blinking the LEDs.
        """
        self.message = message
        self.colour = RGBColor.fromHEX(hex_colour)
        # A list of booleans; the item at index i indicates whether the LEDs
        # should be illuminated during that "tick"
        self.schedule = []
        # Holds our current index in the schedule
        self.tick = 0

        for idx, char in enumerate(self.message.upper()):
            try:
                morse_sequence = ASCII_UPPERCASE_TO_MORSE[char]
            except:
                raise ValueError(
                    f"Cannot translate character '{char}' (at index {idx}) to Morse (allowed values are: {list(ASCII_UPPERCASE_TO_MORSE.keys())})"
                )

            # Time for the main ASCII -> Morse logic. The numbered items below
            # are the rules, per
            # https://commons.wikimedia.org/wiki/File:International_Morse_Code.svg#/media/File:International_Morse_Code.svg
            # The logic for adding spaces within/between letters is
            # intentionally simplified to avoid needing to look ahead in the
            # message; if this algorithm produces an incorrect result for your
            # message, simply do not send that particular message. :-)
            for morse_letter in morse_sequence:
                match morse_letter:
                    # 1. The length of a dot is one unit.
                    case Morse.DOT:
                        self.schedule.extend([True])
                    # 2. A dash is three units.
                    case Morse.DASH:
                        self.schedule.extend([True] * 3)
                    # 5. The space between words is seven units.
                    # Okay, this one is a little ugly; it's in the same spirit
                    # as rule 4 below. Per the other rules, we added three off
                    # units at the end of the previous letter. That same logic
                    # will add three more off units after this current letter.
                    # So our "space" character itself only needs to add a
                    # single off unit: together that gives us:
                    # 3 (trailing previously) +
                    # 1 (this character) +
                    # 1 + 2 (trailing after this character)
                    # = 7 off units, as required.
                    case Morse.SPACE:
                        self.schedule.extend([False])
                    case x:
                        raise RuntimeError(
                            f"Encountered unrecognized Morse sequence '{x}'; aborting"
                        )
                # 3. The space between parts of the same letter is one unit.
                self.schedule.extend([False])
            # 4. The space between letters is three units.
            # Per rule 3, we've already added one trailing "off" unit. So if
            # we're at the end of a letter, add two more to get us to the
            # required three total.
            self.schedule.extend([False] * 2)

        self.schedule_len = len(self.schedule)

    def display(self, num_leds):
        colour = self.colour if self.schedule[self.tick] else LED_OFF
        self.tick = (self.tick + 1) % self.schedule_len
        return [colour] * num_leds
