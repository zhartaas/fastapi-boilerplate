from fastapi import Depends, HTTPException, status


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateShanyraqRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyraqResponse(AppModel):
    id: str


@router.post(
    "/shanyraqs",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateShanyraqResponse,
)
def create_shanyraq(
    input: CreateShanyraqRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id

    print(input.dict())

    res = str(svc.repository.create_shanyraq(user_id, input.dict()))

    return CreateShanyraqResponse(id=res)
