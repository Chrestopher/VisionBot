# import your test files here

import test.test_itemdex as test_itemdex
import test.test_math as test_math
import test.test_profile as test_profile

if __name__ == '__main__':
    # run the tests here

    test_itemdex.run_tests()
    test_math.run_tests()
    test_profile.run_tests()
