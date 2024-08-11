import unittest

from pyawsopstoolkit_advsearch.search import _match_condition, OR, AND


class TestMatchCondition(unittest.TestCase):
    def test_match_condition_or_true(self):
        self.assertTrue(_match_condition("admin", "Administrator", OR, False))

    def test_match_condition_or_false(self):
        self.assertFalse(_match_condition("admin", "User", OR, False))

    def test_match_condition_and_false(self):
        self.assertFalse(_match_condition("admin", "User", AND, True))

    def test_match_condition_and_true(self):
        self.assertTrue(_match_condition("admin", "Administrator", AND, True))

    def test_match_condition_or_already_matched(self):
        self.assertTrue(_match_condition("admin", "User", OR, True))

    def test_match_condition_and_already_not_matched(self):
        self.assertFalse(_match_condition("admin", "User", AND, False))

    def test_match_condition_case_insensitive(self):
        self.assertTrue(_match_condition("ADMIN", "administrator", OR, False))

    def test_match_condition_empty_value(self):
        self.assertFalse(_match_condition("", "User", OR, False))

    def test_match_condition_empty_role_field(self):
        self.assertFalse(_match_condition("admin", "", OR, False))

    def test_match_condition_empty_value_and_role_field(self):
        self.assertFalse(_match_condition("", "", OR, False))

    def test_match_condition_none_condition(self):
        self.assertFalse(_match_condition("admin", "Administrator", None, False))

    def test_match_condition_list_none_condition(self):
        self.assertFalse(_match_condition("admin", [], None, False))

    def test_match_condition_list_empty_value_and_role_field(self):
        self.assertFalse(_match_condition("", [], OR, False))

    def test_match_condition_list_valid(self):
        self.assertTrue(_match_condition("admin", ["admin", "sample"], OR, False))

    def test_match_condition_list_invalid(self):
        self.assertFalse(_match_condition("admin", ["sample", "test"], OR, False))


if __name__ == '__main__':
    unittest.main()
