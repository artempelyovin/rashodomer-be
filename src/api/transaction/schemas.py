from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel
from core.enums import TransactionType

IdDesc = "Unique ID of the transaction"
IdExamples = ["88085c3e-4622-4fb8-9490-45309162f785"]
AmountDesc = "The amount of the transaction"
AmountExamples = [45]
DescriptionDesc = "Description of the transaction"
DescriptionExamples = ["Buying the bread at the store"]
TransactionTypeDesc = "The type of transaction"
TransactionTypeExamples = [TransactionType.EXPENSE]
BudgetIDDesc = "Budget ID for which this transaction was made"
BudgetIDExamples = ["bbe29f27-a1ff-4d44-a388-989dee864cf7"]
CategoryIdDesc = "Category ID for which this transaction was made"
CategoryIDExamples = ["b9acbf48-37fe-4e93-a95b-a38c56af804d"]
UserIDDesc = "ID of user who created this transaction"
UserIDExamples = ["2543ec71-22d6-47ae-8a1e-9441d050f17e"]
TimestampDesc = "Timestamp when the transaction was made"


class CreateTransactionSchema(FromAttributeModel):
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    type: TransactionType = Field(..., description=TransactionTypeDesc, examples=TransactionTypeExamples)
    budget_id: Annotated[str, UUID] = Field(..., description=BudgetIDDesc, examples=BudgetIDExamples)
    category_id: Annotated[str, UUID] = Field(..., description=CategoryIdDesc, examples=CategoryIDExamples)
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the transaction was made. Now by default"
    )


class TransactionSchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(..., description=IdDesc, examples=IdExamples)
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    type: TransactionType = Field(..., description=TransactionTypeDesc, examples=TransactionTypeExamples)
    budget_id: Annotated[str, UUID] = Field(..., description=BudgetIDDesc, examples=BudgetIDExamples)
    category_id: Annotated[str, UUID] = Field(..., description=CategoryIdDesc, examples=CategoryIDExamples)
    user_id: Annotated[str, UUID] = Field(..., description=UserIDDesc, examples=UserIDExamples)
    timestamp: datetime = Field(..., description=TimestampDesc)
