from decimal import Decimal, InvalidOperation


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str):
            raise TypeError("Имя владельца должно быть строкой")
        if not owner.strip():
            raise ValueError("Имя владельца не может быть пустым")
        if not isinstance(account_number, str):
            raise TypeError("Номер счёта должен быть строкой")
        if not account_number.strip():
            raise ValueError("Номер счёта не может быть пустым")

        self.owner = owner
        self.account_number = account_number
        self._balance = Decimal("0")

    @property
    def balance(self):
        return self._balance

    @staticmethod
    def _validate_amount(amount):
        if isinstance(amount, bool) or not isinstance(amount, (int, float, Decimal)):
            raise TypeError("Сумма должна быть числом")

        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Сумма должна быть конечным числом") from None

        if not value.is_finite():
            raise ValueError("Сумма должна быть конечным числом")
        if value <= 0:
            raise ValueError("Сумма должна быть положительной")
        return value

    def deposit(self, amount):
        value = self._validate_amount(amount)
        self._balance += value
        return self._balance

    def withdraw(self, amount):
        value = self._validate_amount(amount)
        if value > self._balance:
            raise ValueError("Недостаточно средств на счёте")
        self._balance -= value
        return self._balance

    def transfer(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            raise TypeError("Получатель должен быть банковским счётом")
        if recipient is self:
            raise ValueError("Нельзя перевести деньги на тот же счёт")

        value = self._validate_amount(amount)
        if value > self._balance:
            raise ValueError("Недостаточно средств на счёте")

        self._balance -= value
        recipient._balance += value

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0