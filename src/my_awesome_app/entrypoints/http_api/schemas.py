from decimal import Decimal

from pydantic import BaseModel

from my_awesome_app.business.value_objects import Operation


class CalculateInput(BaseModel):
    a: Decimal
    operation: Operation
    b: Decimal
