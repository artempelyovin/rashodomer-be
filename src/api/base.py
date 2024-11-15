from collections.abc import Iterable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from starlette import status


class FromAttributeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


PydanticSchema = TypeVar("PydanticSchema", bound=FromAttributeModel)


class _BaseResponse(BaseModel, Generic[PydanticSchema]):
    data: Any | None = None
    status_code: int = Field(default=status.HTTP_200_OK, description="HTTP status code")
    error: bool = Field(
        default=False,
        description="Presence of an error (`true` if there is an error and `false` otherwise)",
    )
    detail: str | None = Field(
        default=None, description="Detailed description of the error (`null` if there is no error)", examples=[None]
    )


class APIResponse(_BaseResponse[PydanticSchema]):
    data: PydanticSchema | None = Field(None, description="Useful content (`null` if there is an error)")


class APIResponseList(_BaseResponse[PydanticSchema]):
    data: list[PydanticSchema] = Field(default_factory=list, description="Useful content (`null` if there is an error)")


def write_response(
    content: Any,
    schema: type[PydanticSchema],
    *,
    status_code: int = status.HTTP_200_OK,
    error: bool = False,
    detail: str | None = None,
) -> APIResponse[PydanticSchema]:
    return APIResponse[schema](  # type: ignore[valid-type]
        data=content,
        status_code=status_code,
        error=error,
        detail=detail,
    )


def write_response_list(
    content: Iterable[Any],
    schema: type[PydanticSchema],
    *,
    status_code: int = status.HTTP_200_OK,
    error: bool = False,
    detail: str | None = None,
) -> APIResponseList[PydanticSchema]:
    return APIResponseList[schema](  # type: ignore[valid-type]
        data=content,  # type: ignore[arg-type]
        status_code=status_code,
        error=error,
        detail=detail,
    )
