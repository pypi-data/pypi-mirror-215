import unittest
from ..src.describe import (
  desc
)


class DescTest(unittest.TestCase):
    def test_desc(self) -> None:
        self.assertRaises(AssertionError, desc)

