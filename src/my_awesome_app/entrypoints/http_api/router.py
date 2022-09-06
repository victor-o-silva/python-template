from fastapi import APIRouter, Depends

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.use_cases.execute_operation import ExecuteOperationUseCase
from my_awesome_app.entrypoints.http_api import dependencies
from my_awesome_app.entrypoints.http_api.schemas import CalculateInput
from my_awesome_app.settings import Settings

main_router = APIRouter(tags=['main'])


@main_router.post('/calc', response_model=OperationExecution)
async def calculate(
    # request data:
    payload: CalculateInput,
    # other dependencies:
    settings: Settings = Depends(dependencies.get_settings)
):
    use_case = ExecuteOperationUseCase(raise_error_on_div_by_zero=settings.RAISE_ERROR_ON_DIVISION_BY_ZERO)
    result = await use_case.run(a=payload.a, operation=payload.operation, b=payload.b)
    return result
