from unittest import TestCase
from rsled_api.interpolate import interpolate, XYPair

class TestInterpolate(TestCase):
    def test_case_1(self):
        TEST_CASE_1 = [
            XYPair(9000, [0, 100]),
            XYPair(12000, [100, 100]),
            XYPair(15000, [100, 50]),
            XYPair(20000, [100, 25]),
            XYPair(23000, [100, 5]),
        ]

        assert interpolate(TEST_CASE_1, 6000) == [-100.0, 100.0]
        assert interpolate(TEST_CASE_1, 7500) == [-50.0, 100.0]
        assert interpolate(TEST_CASE_1, 9000) == [0.0, 100.0]
        assert interpolate(TEST_CASE_1, 10500) == [50.0, 100.0]
        assert interpolate(TEST_CASE_1, 12000) == [100.0, 100.0]
        assert interpolate(TEST_CASE_1, 15000) == [100.0, 50.0]
        assert interpolate(TEST_CASE_1, 20000) == [100.0, 25.0]
        assert interpolate(TEST_CASE_1, 23000) == [100.0, 5.0]
        assert interpolate(TEST_CASE_1, 26000) == [100.0, -15.0]

    def test_case_2(self):
        TEST_CASE_2 = [
            XYPair(9000, 100),
            XYPair(12000, 75),
            XYPair(15000, 50.0),
            XYPair(20000, 25),
            XYPair(23000, 5),
        ]

        assert interpolate(TEST_CASE_2, 6000) == 125.0
        assert interpolate(TEST_CASE_2, 7500) == 112.5
        assert interpolate(TEST_CASE_2, 9000) == 100.0
        assert interpolate(TEST_CASE_2, 10500) == 175.0 / 2.0
        assert interpolate(TEST_CASE_2, 12000) == 75.0
        assert interpolate(TEST_CASE_2, 14000) == 50.0 + (25.0 / 3.0)
        assert interpolate(TEST_CASE_2, 15000) == 50.0
        assert interpolate(TEST_CASE_2, 20000) == 25.0
        assert interpolate(TEST_CASE_2, 23000) == 5.0
        assert interpolate(TEST_CASE_2, 26000) == -15.0
