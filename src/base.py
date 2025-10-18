from collections.abc import Iterable
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from starlette import status

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


class _BaseResponse(BaseModel, Generic[PydanticSchema]):
    result: Any | None = None
    status_code: int = Field(default=status.HTTP_200_OK, description="HTTP status code")
    error: ErrorSchema | None = Field(
        default=None, description="Details of the error, if any (otherwise `null`)", examples=[None]
    )


class APIResponse(_BaseResponse[PydanticSchema]):
    result: PydanticSchema | None = Field(None, description="Useful content (`null` if there is an error)")


class ResultListSchema(BaseModel, Generic[PydanticSchema]):
    total: int = Field(..., ge=0, examples=[1])
    limit: int | None = Field(None, ge=0)
    offset: int = Field(0, ge=0)
    items: list[PydanticSchema]


class APIResponseList(_BaseResponse[PydanticSchema]):
    result: ResultListSchema[PydanticSchema] = Field(
        default_factory=list, description="Useful content (`null` if there is an error)"
    )


def write_response(
    result: Any, schema: type[PydanticSchema], *, status_code: int = status.HTTP_200_OK
) -> APIResponse[PydanticSchema]:
    return APIResponse[schema](result=result, status_code=status_code, error=None)  # type: ignore[valid-type]


def write_response_list(
    total: int,
    items: Iterable[Any],
    schema: type[PydanticSchema],
    *,
    limit: int | None = None,
    offset: int = 0,
    status_code: int = status.HTTP_200_OK,
) -> APIResponseList[PydanticSchema]:
    return APIResponseList[schema].model_validate(  # type: ignore[valid-type]
        {
            "result": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "items": items,
            },
            "status_code": status_code,
            "error": None,
        }
    )
