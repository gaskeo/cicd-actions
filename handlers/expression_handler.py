from typing import Literal, Type

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class DetailExceptionResponse(BaseModel):
    detail: str


class ExpressionResponse(BaseModel):
    answer: float


class ExpressionSolver:
    def __init__(self, number1: float, number2: float):
        self.number1 = number1
        self.number2 = number2

    def solve(self) -> float:
        ...


class SumSolver(ExpressionSolver):
    def solve(self) -> float:
        return self.number1 + self.number2


class DifferenceSolver(ExpressionSolver):
    def solve(self) -> float:
        return self.number1 - self.number2


class MultiplicationSolver(ExpressionSolver):
    def solve(self) -> float:
        return self.number1 * self.number2


class DivisionSolver(ExpressionSolver):
    def solve(self) -> float:
        return self.number1 / self.number2


def create_expression_handler(app: FastAPI):
    @app.get("/expression", response_model=ExpressionResponse, responses={
        status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: {"model": DetailExceptionResponse}
    },
             description='This handler can calculate simple expressions with +, -, * and / operations.')
    def expression_handler(number1: float, number2: float, operation: Literal["+", "-", "*", "/"]):
        expression_solver: Type[ExpressionSolver] = ...
        if operation == "+":
            expression_solver = SumSolver
        if operation == "-":
            expression_solver = DifferenceSolver
        if operation == "*":
            expression_solver = MultiplicationSolver
        if operation == "/":
            expression_solver = DivisionSolver
        try:
            return {"answer": expression_solver(number1, number2).solve()}
        except ZeroDivisionError:
            return JSONResponse(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                                content={"detail": "Division by zero"})
