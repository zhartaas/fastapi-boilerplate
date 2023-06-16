from fastapi import Depends

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import HTTPException


class GetMyShanyraqResponse(AppModel):
    allShanyraqs = []


@router.get("/shanyraks/{id}", response_model=GetMyShanyraqResponse)
def get_my_shanyraq(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.repository.get_my_shanyraq_by_id(jwt_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return GetMyShanyraqResponse(allShanyraqs=user)
