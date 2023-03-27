from typing import Literal, Type

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class Expression(BaseModel):
    number1: float
    number2: float
    operation: Literal["+", "-", "*", "/"]


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
    @app.get("/expression")
    def expression_handler(expression: Expression):
        expression_solver: Type[ExpressionSolver] = ...
        if expression.operation == "+":
            expression_solver = SumSolver
        if expression.operation == "-":
            expression_solver = DifferenceSolver
        if expression.operation == "*":
            expression_solver = MultiplicationSolver
        if expression.operation == "/":
            expression_solver = DivisionSolver
        try:
            return expression_solver(expression.number1, expression.number2).solve()
        except ZeroDivisionError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Division by zero")

