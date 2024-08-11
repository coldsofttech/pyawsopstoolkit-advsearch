import unittest

from pyawsopstoolkit_advsearch.search import _match_number_condition, OR, AND


class TestMatchNumberCondition(unittest.TestCase):
    def test_single_value_or_condition(self):
        self.assertTrue(_match_number_condition(5, 5, OR, False))
        self.assertTrue(_match_number_condition(5, 5, OR, True))
        self.assertTrue(_match_number_condition(5, [5], OR, False))
        self.assertTrue(_match_number_condition(5, [5], OR, True))
        self.assertTrue(_match_number_condition(5, [4, 5, 6], OR, False))
        self.assertTrue(_match_number_condition(5, [4, 5, 6], OR, True))
        self.assertFalse(_match_number_condition(5, [4, 6], OR, False))
        self.assertTrue(_match_number_condition(5, [4, 6], OR, True))

    def test_single_value_and_condition(self):
        self.assertTrue(_match_number_condition(5, 5, AND, False))
        self.assertTrue(_match_number_condition(5, 5, AND, True))
        self.assertTrue(_match_number_condition(5, [5], AND, False))
        self.assertTrue(_match_number_condition(5, [5], AND, True))
        self.assertTrue(_match_number_condition(5, [4, 5, 6], AND, False))
        self.assertTrue(_match_number_condition(5, [4, 5, 6], AND, True))
        self.assertFalse(_match_number_condition(5, [4, 6], AND, False))
        self.assertFalse(_match_number_condition(5, [4, 6], AND, True))

    def test_invalid_condition(self):
        self.assertFalse(_match_number_condition(5, 5, 'INVALID', False))
        self.assertTrue(_match_number_condition(5, 5, 'INVALID', True))

    def test_no_value(self):
        self.assertFalse(_match_number_condition(None, 5, OR, False))
        self.assertFalse(_match_number_condition(0, 5, OR, False))
        self.assertFalse(_match_number_condition(None, [5], OR, False))
        self.assertFalse(_match_number_condition(0, [5], OR, False))

    def test_no_search_field(self):
        self.assertFalse(_match_number_condition(5, None, OR, False))
        self.assertFalse(_match_number_condition(5, 0, OR, False))
        self.assertFalse(_match_number_condition(5, [], OR, False))

    def test_empty_list_search_field(self):
        self.assertFalse(_match_number_condition(5, [], OR, False))
        self.assertFalse(_match_number_condition(5, [], AND, True))


if __name__ == '__main__':
    unittest.main()
