from asteria.scales import *

from pytest import approx


class TestLinearScale:
    def test_basic(self):
        scaled = linear(lambda: 20, 0, 40)
        assert scaled() == approx(0.5)

    def test_offset(self):
        scaled = linear(lambda: 20, 10, 70)
        assert scaled() == approx(1 / 6)

    def test_too_low(self):
        scaled = linear(lambda: 20, 60, 70)
        assert scaled() == approx(0)

    def test_too_high(self):
        scaled = linear(lambda: 100, 10, 70)
        assert scaled() == approx(1)
