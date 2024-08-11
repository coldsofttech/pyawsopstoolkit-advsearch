import unittest

from pyawsopstoolkit_advsearch.exceptions import AdvanceSearchError


class TestAdvanceSearchError(unittest.TestCase):
    def setUp(self) -> None:
        self.message = 'test message'
        self.exception = ValueError('invalid value')
        self.advance_search_error = AdvanceSearchError(self.message)
        self.advance_search_error_with_exception = AdvanceSearchError(self.message, self.exception)

    def test_initialization(self):
        self.assertEqual(self.advance_search_error.message, f'ERROR: {self.message}.')
        self.assertIsNone(self.advance_search_error.exception)

    def test_initialization_with_exception(self):
        self.assertEqual(self.advance_search_error_with_exception.message, f'ERROR: {self.message}. {self.exception}.')
        self.assertEqual(self.advance_search_error_with_exception.exception, self.exception)


if __name__ == "__main__":
    unittest.main()
