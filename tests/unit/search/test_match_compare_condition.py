import unittest
from datetime import datetime

from pyawsopstoolkit_advsearch.search import _match_compare_condition, LESS_THAN, AND, LESS_THAN_OR_EQUAL_TO, \
    EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, GREATER_THAN_OR_EQUAL_TO, BETWEEN, OR


class TestMatchCompareCondition(unittest.TestCase):
    def test_less_than(self):
        self.assertTrue(_match_compare_condition({LESS_THAN: 10}, 5, AND, True))
        self.assertFalse(_match_compare_condition({LESS_THAN: 10}, 15, AND, True))

    def test_less_than_or_equal_to(self):
        self.assertTrue(_match_compare_condition({LESS_THAN_OR_EQUAL_TO: 10}, 10, AND, True))
        self.assertFalse(_match_compare_condition({LESS_THAN_OR_EQUAL_TO: 10}, 15, AND, True))

    def test_equal_to(self):
        self.assertTrue(_match_compare_condition({EQUAL_TO: 10}, 10, AND, True))
        self.assertFalse(_match_compare_condition({EQUAL_TO: 10}, 5, AND, True))

    def test_not_equal_to(self):
        self.assertTrue(_match_compare_condition({NOT_EQUAL_TO: 10}, 5, AND, True))
        self.assertFalse(_match_compare_condition({NOT_EQUAL_TO: 10}, 10, AND, True))

    def test_greater_than(self):
        self.assertTrue(_match_compare_condition({GREATER_THAN: 10}, 15, AND, True))
        self.assertFalse(_match_compare_condition({GREATER_THAN: 10}, 5, AND, True))

    def test_greater_than_or_equal_to(self):
        self.assertTrue(_match_compare_condition({GREATER_THAN_OR_EQUAL_TO: 10}, 10, AND, True))
        self.assertFalse(_match_compare_condition({GREATER_THAN_OR_EQUAL_TO: 10}, 5, AND, True))

    def test_between(self):
        self.assertTrue(_match_compare_condition({BETWEEN: [5, 15]}, 10, AND, True))
        self.assertFalse(_match_compare_condition({BETWEEN: [5, 15]}, 20, AND, True))
        self.assertRaises(ValueError, _match_compare_condition, {BETWEEN: [5]}, 10, AND, True)
        self.assertRaises(ValueError, _match_compare_condition, {BETWEEN: "5,15"}, 10, AND, True)

    def test_datetime_comparison(self):
        self.assertTrue(_match_compare_condition({LESS_THAN: "2024-01-01T00:00:00"}, datetime(2023, 12, 31), AND, True))
        self.assertFalse(
            _match_compare_condition({LESS_THAN: "2023-01-01T00:00:00"}, datetime(2023, 12, 31), AND, True)
        )
        self.assertTrue(
            _match_compare_condition(
                {BETWEEN: ["2023-01-01T00:00:00", "2024-01-01T00:00:00"]}, datetime(2023, 6, 1), AND, True
            )
        )

    def test_invalid_value_dict(self):
        self.assertRaises(ValueError, _match_compare_condition, "invalid", 10, AND, True)

    def test_or_condition(self):
        self.assertTrue(_match_compare_condition({EQUAL_TO: 10}, 10, OR, False))
        self.assertTrue(_match_compare_condition({EQUAL_TO: 10}, 5, OR, True))
        self.assertFalse(_match_compare_condition({EQUAL_TO: 10}, 5, OR, False))

    def test_and_condition(self):
        self.assertTrue(_match_compare_condition({EQUAL_TO: 10}, 10, AND, True))
        self.assertFalse(_match_compare_condition({EQUAL_TO: 10}, 5, AND, True))
        self.assertFalse(_match_compare_condition({EQUAL_TO: 10}, 10, AND, False))


if __name__ == "__main__":
    unittest.main()
