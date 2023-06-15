from fastapi import Depends, Response


from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class UpdateMyShanyraqRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def update_my_shanyraq(
    input: UpdateMyShanyraqRequest,
    shanyrak_id=str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    url = svc.repository.insert_media(jwt_data.user_id, shanyrak_id, input.dict())

    return {"url": url}
