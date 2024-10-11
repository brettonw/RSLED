from unittest import TestCase
from rsled_api.utility import clamp, clamp_array

class TestUtility(TestCase):
    def test_clamp(self):
        assert clamp(-1, 0, 2) == 0
        assert clamp(0, 0, 2) == 0
        assert clamp(1, 0, 2) == 1
        assert clamp(2, 0, 2) == 2
        assert clamp(3, 0, 2) == 2

    def test_clamp_array(self):
        assert clamp_array([-1, 0], 0, 2) == [0, 0]
        assert clamp_array([0, 0], 0, 2) == [0, 0]
        assert clamp_array([1, 0], 0, 2) == [1, 0]
        assert clamp_array([2, 0], 0, 2) == [2, 0]
        assert clamp_array([3, 0], 0, 2) == [2, 0]

        assert clamp_array([0, -1, 0], 0, 2) == [0, 0, 0]
        assert clamp_array([0, 0, 0], 0, 2) == [0, 0, 0]
        assert clamp_array([0, 1, 0], 0, 2) == [0, 1, 0]
        assert clamp_array([0, 2, 0], 0, 2) == [0, 2, 0]
        assert clamp_array([0, 3, 0], 0, 2) == [0, 2, 0]
