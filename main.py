import os
import re


class PasswordValidator:
    PATTERN: str = r'(\w) (\d+)-(\d+): (\w+)'

    def __init__(self, filename: str):
        self.filename = self._validate_file(filename)

    @staticmethod
    def _validate_file(filename: str) -> str:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File {filename} not found")
        elif os.path.getsize(filename) == 0:
            raise ValueError("File {filename} is empty")
        return filename

    @staticmethod
    def _is_valid_range(min_range: int, max_range: int) -> bool:
        return max_range > min_range

    def _is_valid_password(self, line: str) -> bool:
        match = re.match(self.PATTERN, line)
        if not match:
            return False
        char, min_count, max_count, password = match.groups()

        if not self._is_valid_range(int(min_count), int(max_count)):
            return False

        count = password.count(char)
        if count < int(min_count) or count > int(max_count):
            return False

        return True

    def get_count_valid_passwords(self) -> int:
        valid_passwords_count = 0
        with open(self.filename) as f:
            for line in f:
                if self._is_valid_password(line.strip()):
                    valid_passwords_count += 1

        return valid_passwords_count


if __name__ == "__main__":
    print(PasswordValidator('test.txt').get_count_valid_passwords())
