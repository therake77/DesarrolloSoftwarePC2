from dataclasses import dataclass
from datetime import date
from domain.enums.estado_prestamos import EstadoPrestamo
from typing import Optional

@dataclass
class Loan:
    id: Optional[int]
    user_id: int
    copy_code: str
    aproval_date: Optional[date]
    due_date: Optional[date]
    retrival_date: Optional[date]
    status: EstadoPrestamo


class LoanBuilder:
    def __init__(self):
        self._id = None
        self._user_id = None
        self._copy_code = None
        self._aproval_date = None
        self._due_date = None
        self._retrival_date = None
        self._status = None

    def set_id(self, id: int):
        self._id = id
        return self

    def set_user_id(self, user_id: int):
        self._user_id = user_id
        return self

    def set_copy_code(self, copy_code: str):
        self._copy_code = copy_code
        return self

    def set_aproval_date(self, aproval_date: date):
        if self._due_date and aproval_date > self._due_date:
            raise ValueError("Aproval date cannot be after due date.")
        self._aproval_date = aproval_date
        return self

    def set_due_date(self, due_date: date):
        if self._aproval_date and due_date < self._aproval_date:
            raise ValueError("Due date cannot be before aproval date.")
        self._due_date = due_date
        return self

    def set_retrival_date(self, retrival_date: date):
        if self._aproval_date and retrival_date < self._aproval_date:
            raise ValueError("Retrival date cannot be before aproval date.")
        self._retrival_date = retrival_date
        return self

    def set_status(self, status: EstadoPrestamo):
        self._status = status
        return self

    def build(self) -> Loan:
        return Loan(
            id=self._id,
            user_id=self._user_id,
            copy_code=self._copy_code,
            aproval_date=self._aproval_date,
            due_date=self._due_date,
            retrival_date=self._retrival_date,
            status=self._status
        )