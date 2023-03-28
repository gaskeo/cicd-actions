from fastapi import FastAPI, status, Query, Response
from fastapi.responses import JSONResponse

from typing import Literal, Type, Annotated
from pydantic import BaseModel

from handlers.error_handlers import ErrorCodes, DetailExceptionResponse, ExpressionErrorResponse, InvalidDataResponse


class ExpressionResponse(BaseModel):
    answer: float
    expression: str

    class Config:
        schema_extra = {
            "example": {
                "answer": 7.4,
                "expression": "2.3 + 5.1"
            }
        }


class ExpressionSolver:
    operation = ""

    def __init__(self, number1: float, number2: float):
        self.number1 = number1
        self.number2 = number2

    def solve(self) -> float:
        ...

    def expression(self):
        return f"{self.number1} {self.operation} {self.number2}"


class SumSolver(ExpressionSolver):
    operation = "+"

    def solve(self) -> float:
        return self.number1 + self.number2


class DifferenceSolver(ExpressionSolver):
    operation = "-"

    def solve(self) -> float:
        return self.number1 - self.number2


class MultiplicationSolver(ExpressionSolver):
    operation = "*"

    def solve(self) -> float:
        return self.number1 * self.number2


class DivisionSolver(ExpressionSolver):
    operation = "/"

    def solve(self) -> float:
        return self.number1 / self.number2


def create_expression_handler(app: FastAPI):
    @app.get(
        "/expression", response_model=ExpressionResponse, responses={
            status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: {"model": ExpressionErrorResponse},
            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": InvalidDataResponse}
        },
        description='This handler can calculate simple expressions '
                    'with  **[a]ddition**, **[s]ubtraction**, '
                    '**[m]ultiplication** and **[d]ivision** operations.',
    )
    def expression_handler(n1: Annotated[float, Query(description="First number in expression", example=1.5)],
                           n2: Annotated[float, Query(description="Second number in expression", example=5.2)],
                           operation: Annotated[Literal["a", "s", "m", "d"], Query(
                               description="Operation. **[a]ddition**, **[s]ubtraction**, "
                                           "**[m]ultiplication** and **[d]ivision**")]):
        expression_solver: Type[ExpressionSolver] = ...
        if operation == "a":
            expression_solver = SumSolver
        if operation == "s":
            expression_solver = DifferenceSolver
        if operation == "m":
            expression_solver = MultiplicationSolver
        if operation == "d":
            expression_solver = DivisionSolver
        try:
            return {"answer": expression_solver(n1, n2).solve(), "expression": expression_solver(n1, n2).expression()}
        except ZeroDivisionError:
            return JSONResponse(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                                content={"code": ErrorCodes.INVALID_EXPRESSION, "message": "division by zero"})
