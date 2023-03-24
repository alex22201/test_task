import os
import unittest
import tempfile
from main import PasswordValidator


class TestPasswordValidator(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('a 1-5: abcde\nb 2-4: bbbbb\n')
        self.validator = PasswordValidator(f.name)

    def test_valid_file(self):
        self.assertEqual(self.validator.get_count_valid_passwords(), 1)

    def test_file_not_found(self):
        with self.assertRaises(BaseException):
            PasswordValidator('nonexistent.txt')

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            pass
        with self.assertRaises(BaseException):
            PasswordValidator(f.name)
        os.unlink(f.name)

    def test_invalid_range(self):
        self.assertFalse(self.validator._is_valid_range(5, 3))

    def test_valid_password(self):
        self.assertTrue(self.validator._is_valid_password('a 1-5: abcde'))
        self.assertTrue(self.validator._is_valid_password('a 1-2: abcde'))
        self.assertFalse(self.validator._is_valid_password('a 1-2: bcde'))
        self.assertFalse(self.validator._is_valid_password('b 2-4: aaaaa'))
        self.assertFalse(self.validator._is_valid_password('a 2-4: zzzz'))


if __name__ == '__main__':
    unittest.main()
