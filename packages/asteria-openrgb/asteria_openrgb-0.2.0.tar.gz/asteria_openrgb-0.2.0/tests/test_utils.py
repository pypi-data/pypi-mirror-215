from asteria.utils import *

from pytest import approx


class TestClamp:
    def test_within_bounds(self):
        assert clamp(0.5) == approx(0.5)

    def test_too_low(self):
        assert clamp(-99) == approx(0)

    def test_too_high(self):
        assert clamp(100.92) == approx(1)
