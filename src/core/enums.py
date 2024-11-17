from enum import Enum


class TransactionType(Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"
