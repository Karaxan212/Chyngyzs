import unittest
from decimal import Decimal

from bank_account import BankAccount


class BankAccountTests(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Анна Иванова", "123456")

    def test_new_account_stores_details_and_starts_empty(self):
        self.assertEqual(self.account.owner, "Анна Иванова")
        self.assertEqual(self.account.account_number, "123456")
        self.assertEqual(self.account.get_balance(), Decimal("0"))
        self.assertTrue(self.account.is_empty())

    def test_deposit_increases_balance(self):
        self.account.deposit(Decimal("125.50"))
        self.assertEqual(self.account.get_balance(), Decimal("125.50"))
        self.assertFalse(self.account.is_empty())

    def test_deposit_rejects_invalid_amount_without_changing_balance(self):
        for amount in (0, -1, float("nan"), float("inf")):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.deposit(amount)
                self.assertEqual(self.account.get_balance(), Decimal("0"))

    def test_deposit_rejects_non_numeric_amount(self):
        with self.assertRaises(TypeError):
            self.account.deposit("сто")

    def test_withdraw_decreases_balance(self):
        self.account.deposit(100)
        self.account.withdraw(35.25)
        self.assertEqual(self.account.get_balance(), Decimal("64.75"))

    def test_withdraw_rejects_insufficient_funds_without_changing_balance(self):
        self.account.deposit(20)
        with self.assertRaises(ValueError):
            self.account.withdraw(21)
        self.assertEqual(self.account.get_balance(), Decimal("20"))

    def test_withdraw_rejects_negative_amount_without_changing_balance(self):
        self.account.deposit(20)
        with self.assertRaises(ValueError):
            self.account.withdraw(-1)
        self.assertEqual(self.account.get_balance(), Decimal("20"))

    def test_transfer_updates_both_balances_by_same_amount(self):
        recipient = BankAccount("Пётр Петров", "654321")
        self.account.deposit(100)

        self.account.transfer(recipient, 30.25)

        self.assertEqual(self.account.get_balance(), Decimal("69.75"))
        self.assertEqual(recipient.get_balance(), Decimal("30.25"))

    def test_failed_transfer_does_not_change_either_balance(self):
        recipient = BankAccount("Пётр Петров", "654321")
        self.account.deposit(10)
        recipient.deposit(5)

        with self.assertRaises(ValueError):
            self.account.transfer(recipient, 11)

        self.assertEqual(self.account.get_balance(), Decimal("10"))
        self.assertEqual(recipient.get_balance(), Decimal("5"))

    def test_transfer_rejects_same_account_without_changing_balance(self):
        self.account.deposit(10)

        with self.assertRaises(ValueError):
            self.account.transfer(self.account, 5)

        self.assertEqual(self.account.get_balance(), Decimal("10"))

    def test_transfer_rejects_non_account_recipient(self):
        with self.assertRaises(TypeError):
            self.account.transfer(None, 1)


if __name__ == "__main__":
    unittest.main()