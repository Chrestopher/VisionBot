import unittest
import custom_math


class Test_math(unittest.TestCase):

    def test_add(self):
        args = ["5", "+", "5"]
        self.assertEqual(custom_math.math(args), "10")
        args1 = ["-5", "+", "5"]
        self.assertEqual(custom_math.math(args1), "0")
        args2 = ["-5", "+", "-5"]
        self.assertEqual(custom_math.math(args2), "-10")

    def test_subtract(self):
        args = ["5", "-", "5"]
        self.assertEqual(custom_math.math(args), "0")
        args1 = ["-5", "-", "5"]
        self.assertEqual(custom_math.math(args1), "-10")
        args2 = ["-5", "-", "-5"]
        self.assertEqual(custom_math.math(args2), "0")

    def test_multiply(self):
        args = ["5", "*", "5"]
        self.assertEqual(custom_math.math(args), "25")
        args1 = ["-5", "*", "5"]
        self.assertEqual(custom_math.math(args1), "-25")
        args2 = ["-5", "*", "-5"]
        self.assertEqual(custom_math.math(args2), "25")

    def test_divide(self):
        args = ["5", "/", "5"]
        self.assertEqual(custom_math.math(args), "1.0")
        args1 = ["-5", "/", "5"]
        self.assertEqual(custom_math.math(args1), "-1.0")
        args2 = ["-5", "/", "-5"]
        self.assertEqual(custom_math.math(args2), "1.0")
        args3 = ["5", "/", "0"]
        with self.assertRaises(ZeroDivisionError):
            custom_math.math(args3)

    def test_errors(self):
        args = ["5", "+", "5", "f"]
        self.assertEqual(custom_math.math(args), "Please put your numbers in the correct order: number operator number")
        args1 = ["f", "+", "a"]
        self.assertEqual(custom_math.math(args1), "Please use real numbers.")
        args2 = ["5", "$", "5"]
        self.assertEqual(custom_math.math(args2), "Please use a supported operation: * - + /")


def create_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(Test_math('test_add'))
    test_suite.addTest(Test_math('test_subtract'))
    test_suite.addTest(Test_math('test_multiply'))
    test_suite.addTest(Test_math('test_divide'))
    test_suite.addTest(Test_math('test_errors'))
    return test_suite


def run_tests():
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    run_tests()
