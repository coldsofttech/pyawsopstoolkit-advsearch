import unittest

from pyawsopstoolkit_advsearch.exceptions import SearchAttributeError


class TestSearchAttributeError(unittest.TestCase):
    def setUp(self) -> None:
        self.message = 'test message'
        self.exception = ValueError('invalid value')
        self.search_attribute_error = SearchAttributeError(self.message)
        self.search_attribute_error_with_exception = SearchAttributeError(self.message, self.exception)

    def test_initialization(self):
        self.assertEqual(self.search_attribute_error.message, f'ERROR: {self.message}.')
        self.assertIsNone(self.search_attribute_error.exception)

    def test_initialization_with_exception(self):
        self.assertEqual(
            self.search_attribute_error_with_exception.message, f'ERROR: {self.message}. {self.exception}.'
        )
        self.assertEqual(self.search_attribute_error_with_exception.exception, self.exception)


if __name__ == "__main__":
    unittest.main()
