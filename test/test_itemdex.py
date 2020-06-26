import unittest
import itemdex


class TestItemdex(unittest.TestCase):
    # define tests here
    def test_that_scrape_retrieves_correct_values(self):
        item_name = "potion"

        expected_item = {}
        expected_item["item_name"] = "Potion"
        expected_item["item_description"] = "Heals a Pokémon by 20HP"
        expected_item["item_image_url"] = "https://serebii.net/itemdex/sprites/pgl/potion.png"
        expected_item["item_type"] = "Recovery"

        actual_item = itemdex.scrape(item_name)
        self.assertEqual(actual_item, expected_item)


def create_suite():
    test_suite = unittest.TestSuite()
    # Add tests here
    test_suite.addTest(TestItemdex('test_that_scrape_retrieves_correct_values'))

    return test_suite


def run_tests():
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    run_tests()
