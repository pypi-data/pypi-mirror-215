import asteria.constants as constants
from asteria.instruments import *

import pytest

TEST_COLOUR_HEX = "#00ff00"
TEST_COLOUR = RGBColor.fromHEX(TEST_COLOUR_HEX)


class TestStaticColour:
    def test_basic(self):
        instrument = StaticColour(TEST_COLOUR_HEX)
        output = instrument.display(4)
        assert len(output) == 4
        assert output[0] == TEST_COLOUR
        assert output[1] == TEST_COLOUR
        assert output[2] == TEST_COLOUR
        assert output[3] == TEST_COLOUR


class TestLinearHueRange:
    def test_basic(self):
        instrument = LinearHueRange(lambda: 0.5, 0, 360)
        output = instrument.display(1)
        assert len(output) == 1
        assert output[0] == RGBColor.fromHSV(180, 100, 100)

    def test_out_of_bounds(self):
        instrument = LinearHueRange(lambda: 42, 0, 180)
        output = instrument.display(1)
        assert len(output) == 1
        assert output[0] == RGBColor.fromHSV(180, 100, 100)


class TestPercentageBar:
    def test_basic(self):
        instrument = PercentageBar(lambda: 0.5, TEST_COLOUR_HEX)
        output = instrument.display(4)
        assert len(output) == 4
        assert output[0] == LED_OFF
        assert output[1] == LED_OFF
        assert output[2] == TEST_COLOUR
        assert output[3] == TEST_COLOUR


class TestMorseCode:
    def test_basic(self):
        instrument = MorseCode("a", TEST_COLOUR_HEX)
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF

    def test_bad_input(self):
        with pytest.raises(ValueError):
            instrument = MorseCode("\N{SMILING FACE WITH SUNGLASSES}")

    # Ensure that the message loops properly
    def test_loop(self):
        instrument = MorseCode("E", TEST_COLOUR_HEX)
        # First iteration
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # Second iteration
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # Third iteration (partial)
        assert instrument.display(1)[0] == TEST_COLOUR

    def test_sos(self):
        instrument = MorseCode("SOS", TEST_COLOUR_HEX)
        # First 'S'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # 'O'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # Second 'S'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF

    # Ensure that spaces are handled correctly. I'm intentionally declaring
    # leading spaces to be out of scope...
    def test_space(self):
        instrument = MorseCode("o m g", TEST_COLOUR_HEX)
        # 'O'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # First space
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # 'M'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # Second space
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        # 'G'
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == TEST_COLOUR
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
        assert instrument.display(1)[0] == constants.LED_OFF
