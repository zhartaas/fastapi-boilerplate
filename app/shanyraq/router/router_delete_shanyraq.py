from fastapi import Depends, Response
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/{shanyrak_id:str}/deleteShanyraq")
def delete_my_shanyraq(
    shanyrak_id=str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.delete_shanyraq(jwt_data.user_id, shanyrak_id)

    return Response(status_code=200)
