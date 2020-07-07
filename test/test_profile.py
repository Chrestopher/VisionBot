import unittest
from unittest.mock import patch
import profile
import json_api

class TestProfile(unittest.TestCase):

    def test_profile_update(self):
        user = 'Khajeet0468'
        avatar_url = "catface"
        args=[]
        self.assertEqual(profile.process_message(user,avatar_url,args),"Update command missing parameters: !profile "
                                                                        "update {category} {value}")
        args1=["update"]
        self.assertEqual(profile.process_message(user,avatar_url,args1),"Update command missing parameters: !profile update {category} {value}")

    @patch('profile.update_account')
    def test_mock_update_account(self,mock_update_account):
        user = 'Khajeet0468'
        avatar_url = "catface"
        args = ["update", "bio", "the goat"]
        profile.process_message(user, avatar_url, args)
        self.assertEqual(mock_update_account.call_count, 1)
        args2=["update","bios","the goat"]

    @patch('profile.update_account')
    def test_mock_update_fail(self,mock_update_account):
        user = 'Khajeet0468'
        avatar_url = "catface"
        args = ["update", "bios", "the goat"]
        profile.process_message(user, avatar_url, args)
        self.assertEqual(mock_update_account.call_count, 0)

    @patch('profile.view_account')
    def test_mock_view_works(self,mock_view):
        user = 'Khajeet0468'
        avatar_url = "catface"
        args= ['view']
        profile.process_message(user,avatar_url,args)
        self.assertEqual(mock_view.call_count, 1)

    @patch('profile.create_account')
    def test_mock_create_works(self,mock_create):
        user = 'Khajeet0468'
        avatar_url = "catface"
        args = ['create']
        profile.process_message(user, avatar_url, args)
        self.assertEqual(mock_create.call_count, 1)


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestProfile('test_profile_update'))
    test_suite.addTest(TestProfile('test_mock_update_account'))
    test_suite.addTest(TestProfile('test_mock_update_fail'))
    test_suite.addTest(TestProfile('test_mock_view_works'))
    test_suite.addTest(TestProfile('test_mock_create_works'))

    return test_suite


def run_tests():
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)