from fastapi import APIRouter, Depends

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.business.use_cases.execute_operation import ExecuteOperationUseCase
from my_awesome_app.business.use_cases.list_operations import ListOperationUseCase
from my_awesome_app.business.utils import GenericPage
from my_awesome_app.entrypoints.http_api import dependencies
from my_awesome_app.entrypoints.http_api.schemas import CalculateInput
from my_awesome_app.entrypoints.http_api.utils import to_json_response
from my_awesome_app.settings import Settings

main_router = APIRouter(tags=['main'])


@main_router.post('/list/', response_model=GenericPage[OperationExecution])
async def list_records(
    # request data:
    limit: int = 10,
    offset: int = 0,
    # other dependencies:
    uow_maker: IUnitOfWorkMaker = Depends(dependencies.get_unit_of_work_maker),
):
    use_case = ListOperationUseCase(uow_maker=uow_maker)
    result = await use_case.run(limit=limit, offset=offset)
    return to_json_response(result)


@main_router.post('/calc/', response_model=OperationExecution)
async def calculate(
    # request data:
    payload: CalculateInput,
    # other dependencies:
    settings: Settings = Depends(dependencies.get_settings),
    uow_maker: IUnitOfWorkMaker = Depends(dependencies.get_unit_of_work_maker),
):
    use_case = ExecuteOperationUseCase(
        uow_maker=uow_maker,
        raise_error_on_div_by_zero=settings.RAISE_ERROR_ON_DIVISION_BY_ZERO
    )
    result = await use_case.run(a=payload.a, operation=payload.operation, b=payload.b)
    return to_json_response(result)
