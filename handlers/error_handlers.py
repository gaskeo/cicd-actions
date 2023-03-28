from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from enum import Enum
from pydantic import BaseModel


class ErrorCodes(str, Enum):
    INVALID_DATA = "INVALID_DATA"
    INVALID_EXPRESSION = "INVALID_EXPRESSION"


class DetailExceptionResponse(BaseModel):
    code: ErrorCodes
    message: str


class InvalidDataResponse(DetailExceptionResponse):
    code: ErrorCodes
    message: str

    class Config:
        schema_extra = {
            "example": {
                "code": ErrorCodes.INVALID_DATA,
                "message": "invalid data: n1: field required"
            }
        }


class ExpressionErrorResponse(DetailExceptionResponse):
    code: ErrorCodes
    message: str

    class Config:
        schema_extra = {
            "example": {
                "code": ErrorCodes.INVALID_EXPRESSION,
                "message": "division by zero"
            }
        }


def create_422_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        def generate_message(error):
            return f"{error['loc'][-1]}: {error['msg']}"

        return JSONResponse({
            "code": ErrorCodes.INVALID_DATA.value,
            "message": f"invalid data: {'; '.join([generate_message(error) for error in exc.errors()])}"
        }, status_code=422)
