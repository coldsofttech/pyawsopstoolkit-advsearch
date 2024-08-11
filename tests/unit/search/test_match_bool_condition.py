import unittest

from pyawsopstoolkit_advsearch.search import _match_bool_condition, OR, AND


class TestMatchBoolCondition(unittest.TestCase):
    def test_value_or_search_field_none(self):
        self.assertFalse(_match_bool_condition(None, True, OR, True))
        self.assertFalse(_match_bool_condition(True, None, AND, True))
        self.assertFalse(_match_bool_condition(None, None, OR, False))

    def test_search_field_single_bool(self):
        self.assertTrue(_match_bool_condition(True, True, OR, False))
        self.assertFalse(_match_bool_condition(False, True, AND, True))

    def test_search_field_list(self):
        self.assertTrue(_match_bool_condition(True, [True, False], OR, False))
        self.assertFalse(_match_bool_condition(False, [True, True], AND, True))

    def test_condition_or(self):
        self.assertTrue(_match_bool_condition(True, True, OR, False))
        self.assertTrue(_match_bool_condition(False, True, OR, True))
        self.assertTrue(_match_bool_condition(False, False, OR, False))

    def test_condition_and(self):
        self.assertTrue(_match_bool_condition(True, True, AND, True))
        self.assertFalse(_match_bool_condition(False, True, AND, True))
        self.assertTrue(_match_bool_condition(True, [True, False], AND, False))

    def test_invalid_condition(self):
        self.assertTrue(_match_bool_condition(True, True, "INVALID", True))
        self.assertFalse(_match_bool_condition(False, True, "INVALID", False))


if __name__ == '__main__':
    unittest.main()
