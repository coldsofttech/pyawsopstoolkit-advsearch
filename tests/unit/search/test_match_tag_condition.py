import unittest

from pyawsopstoolkit_advsearch.search import _match_tag_condition, OR, AND


class TestMatchTagCondition(unittest.TestCase):
    def test_key_only_match(self):
        value = 'tag1'
        tags = ['tag1', 'tag2', 'tag3']
        condition = OR
        matched = True
        key_only = True
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_key_value_match(self):
        value = {'color': 'red', 'size': 'large'}
        tags = {'color': 'red', 'size': 'large'}
        condition = AND
        matched = True
        key_only = False
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_key_value_no_match(self):
        value = {'color': 'red', 'size': 'large'}
        tags = {'color': 'blue', 'size': 'large'}
        condition = AND
        matched = False
        key_only = False
        self.assertFalse(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_condition_or(self):
        value = 'tag1'
        tags = ['tag1', 'tag2', 'tag3']
        condition = OR
        matched = True
        key_only = True
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_condition_and(self):
        value = 'tag1'
        tags = ['tag1', 'tag2', 'tag3']
        condition = AND
        matched = True
        key_only = True
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_matched_true(self):
        value = 'tag1'
        tags = ['tag1', 'tag2', 'tag3']
        condition = OR
        matched = True
        key_only = True
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))

    def test_matched_false(self):
        value = 'tag1'
        tags = ['tag1', 'tag2', 'tag3']
        condition = OR
        matched = False
        key_only = True
        self.assertTrue(_match_tag_condition(value, tags, condition, matched, key_only))


if __name__ == "__main__":
    unittest.main()
