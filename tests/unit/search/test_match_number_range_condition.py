import unittest

from pyawsopstoolkit_advsearch.search import _match_number_range_condition, OR, AND


class TestMatchNumberRangeCondition(unittest.TestCase):
    def test_value_within_range_or_condition(self):
        self.assertTrue(_match_number_range_condition(5, [(1, 10)], OR, False))

    def test_value_within_range_and_condition(self):
        self.assertTrue(_match_number_range_condition(5, [(1, 10)], AND, True))

    def test_value_outside_range_or_condition(self):
        self.assertFalse(_match_number_range_condition(15, [(1, 10)], OR, False))

    def test_value_outside_range_and_condition(self):
        self.assertFalse(_match_number_range_condition(15, [(1, 10)], AND, True))

    def test_no_value(self):
        self.assertFalse(_match_number_range_condition(None, [(1, 10)], OR, False))

    def test_no_search_field(self):
        self.assertFalse(_match_number_range_condition(5, None, OR, False))

    def test_matched_true_or_condition(self):
        self.assertTrue(_match_number_range_condition(15, [(1, 10)], OR, True))

    def test_matched_true_and_condition(self):
        self.assertTrue(_match_number_range_condition(5, [(1, 10)], AND, True))

    def test_condition_with_negative_range(self):
        self.assertTrue(_match_number_range_condition(15, [(1, 10), (-1, -1)], OR, False))

    def test_and_condition_with_negative_range(self):
        self.assertTrue(_match_number_range_condition(15, [(1, 10), (-1, -1)], AND, True))

    def test_and_condition_no_initial_match(self):
        self.assertTrue(_match_number_range_condition(5, [(1, 10)], AND, False))

    def test_invalid_condition(self):
        self.assertFalse(_match_number_range_condition(5, [(1, 10)], 'INVALID', False))


if __name__ == '__main__':
    unittest.main()
