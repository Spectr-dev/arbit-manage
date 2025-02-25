from typing import Any


class StatusQuery:
    def __init__(
        self,
        operation: str = "system",
        result: Any = None,
        comment: str | None = None,
        status: bool = True,
    ):
        self.operation = operation
        self.result = result
        self.comment = comment
        self.status = status

    def __repr__(self):
        return f"StatusQuery<operation: {self.operation}, result: {self.result}, comment: {self.comment}, status: {self.status}>"

    def __str__(self):
        return f"Operation: {self.operation}. Result: {self.result}. Comment: {self.comment}. Status: {self.status}"
