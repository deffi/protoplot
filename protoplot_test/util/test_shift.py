import unittest

from protoplot.util.shift import offset

class TestShift(unittest.TestCase):
    def testNone(self):
        self.assertEqual(offset(None, 4), [0, 0, 0, 0])
        self.assertEqual(offset(None, 5), [0, 0, 0, 0, 0])
        
    def testConstant(self):
        self.assertEqual(offset(0, 4), [0, 0, 0, 0])
        self.assertEqual(offset(0, 5), [0, 0, 0, 0, 0])

        self.assertEqual(offset(1, 4), [-1.5, -0.5, 0.5, 1.5])
        self.assertEqual(offset(1, 5), [-2, -1, 0, 1, 2])
        
    def testList(self):
        self.assertEqual(offset([1, 2.3, 4.56], 3), [1, 2.3, 4.56])    
        with self.assertRaisesRegex(ValueError, "Length of shift_spec does not match count"):
            offset([1, 2.3, 4.56], 4)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()