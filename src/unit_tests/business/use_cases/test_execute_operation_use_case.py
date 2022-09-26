from decimal import Decimal

import pytest

from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.business.use_cases.execute_operation import ExecuteOperationUseCase
from my_awesome_app.business.value_objects import Operation


@pytest.mark.parametrize(
    "a,operation,b,expected_result",
    [
        (Decimal("2"), "+", Decimal("3"), Decimal("5")),
        (Decimal("2"), "-", Decimal("4"), Decimal("-2")),
        (Decimal("2"), "*", Decimal("5"), Decimal("10")),
        (Decimal("2"), "/", Decimal("8"), Decimal("0.25")),
        (Decimal("2"), "^", Decimal("7"), Decimal("128")),
    ],
)
async def test_basic(
    # Fixtures:
    sql_alchemy_uow_maker: IUnitOfWorkMaker,
    # Parametrized:
    a: Decimal,
    operation: Operation,
    b: Decimal,
    expected_result: Decimal,
):
    use_case = ExecuteOperationUseCase(uow_maker=sql_alchemy_uow_maker, raise_error_on_div_by_zero=True)
    execution = await use_case.run(a=a, operation=operation, b=b)
    assert execution.id
    assert execution.result == expected_result

    async with await sql_alchemy_uow_maker() as unit_of_work:
        persisted_execution = await unit_of_work.operation_repository.get_operation(execution.id)

    assert persisted_execution.a == a
    assert persisted_execution.operation == operation
    assert persisted_execution.b == b
    assert persisted_execution.result == expected_result
