
import unittest
from main import printResults, create


class TestFileName(unittest.TestCase):
    cr = create()
    cr.an = "n"

    def get_Input(diet, sorti="prominence", zipcode=10027):
        return zipcode, diet, sorti

    def test_function1(self):
        # self.assertEqual(function1(1), 0)
        results1 = printResults('vegan', "prominence", 10027)
        results2 = printResults('vegan')
        results3 = printResults('vegan', "sorting", 10027)
        results4 = printResults('vegan', "ratings", 10027)
        results5 = printResults('vegan', zipcode=10025)

        '''self.assertEqual(results1, )
        self.assertEqual(results2, 3.3)
        self.assertEqual(results3, 3.3)
        self.assertEqual(results4, 3.3)
        self.assertEqual(results5, 3.3)'''

    def test_function2(self):
        results1 = printResults('hamburgers')
        results2 = printResults('american')
        results3 = printResults('dessert')
        results4 = printResults('mongolian')
        results5 = printResults('nutfree')

        '''self.assertEqual(results1, 3)
        self.assertEqual(results2, 3.3)
        self.assertEqual(results3, 3.3)
        self.assertEqual(results4, 3.3)
        self.assertEqual(results5, 3.3)'''
