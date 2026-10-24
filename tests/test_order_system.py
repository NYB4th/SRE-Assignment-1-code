import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "baseline"))

import legacy_order_system as new
import legacy_order_system_baseline as old

NOTEBOOK = {"name": "Notebook", "category": "book", "price": 300, "qty": 2}
USB = {"name": "USB Drive", "category": "electronics", "price": 800, "qty": 1}


class RegressionTests(unittest.TestCase):
    # Each valid case checks the refactored total against the baseline
    # total for the same input, then against the expected value.

    def check(self, items, customer, delivery, expected):
        before = old.order_total(items, customer, delivery)
        after = new.order_total(items, customer, delivery)
        self.assertEqual(before, after)
        self.assertAlmostEqual(after, expected, places=2)

    def test_regular_customer_no_delivery(self):
        self.check([NOTEBOOK], "regular", "none", 600.00)

    def test_student_discount_standard_delivery(self):
        self.check([NOTEBOOK, USB], "student", "standard", 1360.00)

    def test_staff_discount_express_delivery(self):
        self.check([USB], "staff", "express", 1010.00)

    def test_standard_delivery_regular_customer(self):
        self.check([USB], "regular", "standard", 900.00)

    def test_express_delivery_regular_customer(self):
        self.check([NOTEBOOK], "regular", "express", 850.00)

    def test_receipt_unchanged(self):
        args = ([NOTEBOOK, USB], "student", "standard")
        self.assertEqual(old.print_receipt(*args), new.print_receipt(*args))


class CorrectiveChangeTests(unittest.TestCase):

    def test_negative_quantity_raises(self):
        bad = {"name": "Pen", "category": "other", "price": 50, "qty": -3}
        with self.assertRaises(ValueError):
            new.order_total([bad], "regular", "standard")

    def test_negative_price_raises(self):
        bad = {"name": "Pen", "category": "other", "price": -50, "qty": 3}
        with self.assertRaises(ValueError):
            new.order_total([bad], "regular", "standard")

    def test_receipt_also_rejects_negative_input(self):
        bad = {"name": "Pen", "category": "other", "price": 50, "qty": -1}
        with self.assertRaises(ValueError):
            new.print_receipt([bad], "student", "express")

    def test_baseline_gave_misleading_total(self):
        # Shows the defect: the old code returned a negative total
        bad = {"name": "Pen", "category": "other", "price": 50, "qty": -3}
        self.assertEqual(old.order_total([bad], "regular", "standard"), -50)


if __name__ == "__main__":
    unittest.main()
