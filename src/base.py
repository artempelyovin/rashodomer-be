from collections.abc import Iterable
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

ISO_TIMEZONE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class CustomModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime(ISO_TIMEZONE_FORMAT),  # all dates as ISO with TIMEZONE
        },
    )


PydanticSchema = TypeVar("PydanticSchema", bound=CustomModel)


class ErrorSchema(BaseModel):
    type: str = Field(..., description="Error type")
    detail: str = Field(
        ..., description="Detailed description of the error (`null` if there is no error)", examples=[None]
    )


class ListSchema(BaseModel, Generic[PydanticSchema]):
    total: int = Field(..., ge=0, examples=[1])
    limit: int | None = Field(None, ge=0)
    offset: int = Field(0, ge=0)
    items: list[PydanticSchema]


def write_response_list(
    total: int,
    items: Iterable[Any],
    schema: type[PydanticSchema],
    *,
    limit: int | None = None,
    offset: int = 0,
) -> ListSchema[PydanticSchema]:
    return ListSchema[schema].model_validate(  # type: ignore[valid-type]
        {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items,
        }
    )
