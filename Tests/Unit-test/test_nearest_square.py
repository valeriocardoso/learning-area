from nearest import nearest_square
import unittest


class AddTests(unittest.TestCase):

    def test_nearest_square_5(self):
        self.assertEqual(4, nearest_square(5))

    def test_nearest_square_n12(self):
        self.assertEqual(0, nearest_square(-12))

    def test_nearest_square_9(self):
        self.assertEqual(9, nearest_square(9))

    def test_nearest_square_23(self):
        self.assertEqual(16, nearest_square(23))
