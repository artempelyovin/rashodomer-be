from enum import Enum


class CategoryType(Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"
    TRANSFER = "TRANSFER"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"
