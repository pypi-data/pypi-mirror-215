from abc import ABC, abstractmethod
from openrgb.utils import RGBColor

from ..utils import clamp

LED_OFF = RGBColor.fromHEX("#000000")


class Instrument(ABC):
    """An Instrument determines how the LEDs under its control should be illuminated

    Often, this will involve calling some other function (in our nomenclature,
    a "metric function") and setting the LEDs based on the return value. See
    the `metrics` module for example metric functions. Note also that the
    `scales` module contains helper functions for rescaling metric functions,
    so Instruments do not need to include that logic themselves.

    Note: the metric function (if any) will be provided to the Instrument's
    __init__ as the parameter "metric_function".
    """

    @abstractmethod
    def display(self, num_leds) -> list[RGBColor]:
        """Return a list of length `num_leds` indicating the colours to which the LEDs should be set.

        This will be called periodically by the main thread driving the application.
        """
        raise NotImplementedError()


class StaticColour(Instrument):
    def __init__(self, hex_colour):
        self.hex_colour = hex_colour

    def display(self, num_leds):
        return [RGBColor.fromHEX(self.hex_colour)] * num_leds


class LinearHueRange(Instrument):
    """Gradually transitions between two hues based on the metric_function.

    Note: metric_function is required to produce a value in the range [0, 1].
    """

    # TODO: actually support clockwise argument...
    def __init__(self, metric_function, lower_hue, upper_hue, clockwise=True):
        """
        lower_hue, upper_hue: the starting/ending HSV hues, respectively.
        """
        self.metric_function = metric_function
        self.lower_hue = lower_hue
        self.upper_hue = upper_hue
        self.hue_range = self.upper_hue - self.lower_hue

    def display(self, num_leds):
        # TODO: warn if outside [0, 1]?
        metric_value = clamp(self.metric_function())
        final_hue = RGBColor.fromHSV(
            self.lower_hue + metric_value * self.hue_range, 100, 100
        )
        return [final_hue] * num_leds


class PercentageBar(Instrument):
    """Gradually "fill up" a section of LEDs based on the metric_function.

    When metric_function is 0, all assigned LEDs will be turned off; when it is
    1, all assigned LEDs will be set to hex_colour (and similarly for metric
    values in between).

    Note: metric_function is required to produce a value in the range [0, 1].
    """

    def __init__(self, metric_function, hex_colour, bottom_up=True):
        """
        hex_colour: The hex colour to use for filled LEDs.
        bottom_up: if True, start filling from the "right" side of the list (i.e. highest indices).
        """
        self.metric_function = metric_function
        self.colour = RGBColor.fromHEX(hex_colour)
        self.bottom_up = bottom_up

    def display(self, num_leds):
        # TODO: warn if outside [0, 1]?
        metric_value = clamp(self.metric_function())
        num_filled = round(metric_value * num_leds)
        filled = [self.colour] * num_filled
        empty = [LED_OFF] * (num_leds - num_filled)

        if self.bottom_up:
            return empty + filled
        else:
            return filled + empty


# Beware of circular imports! The morse module needs to import the Instrument
# class we define here, and I want to import the MorseCode class here so that
# it's available as `asteria.instruments.MorseCode`. If you move this import
# _before_ the definition of Instrument, that's a circular import and
# everything will explode.
from .morse import MorseCode
