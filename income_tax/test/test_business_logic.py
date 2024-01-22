from django.test import SimpleTestCase
from income_tax.business_logic.writer import get_income_tax

class BusinessLogicTests(SimpleTestCase):


    def test_get_income_tax_lower_bound(self):
        income = 100000
        result = get_income_tax(income)
        self.assertEqual(result, 13000)

    def test_get_income_tax_higher_bound(self):
        income = 10000000
        result = get_income_tax(income)
        self.assertEqual(result, 1400000)
