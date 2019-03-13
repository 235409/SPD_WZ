import unittest
import flowshop as f
from random import randint


class TestFlow(unittest.TestCase):
    def test_markspan(self):
        self.assertEqual(f.total_makespan([4, 4, 10, 6, 2], [5, 1, 4, 10, 3]), 37)

    def test_johson(self):
        for i in range(3, 10):
            arr1 = [randint(1, 100) for y in range(i)]
            arr2 = [randint(1, 100) for y in range(i)]
            arr = [arr1, arr2]
            with self.subTest(arr=arr):
                self.assertEqual(f.total_makespan(*f.converter(f.johnsons_rule(*arr), *arr)), min(list(f.c_max(*arr))))


if __name__ == '__main__':
    unittest.main()
