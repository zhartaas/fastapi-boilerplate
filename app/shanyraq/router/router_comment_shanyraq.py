from fastapi import Depends, Response
from typing import List
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.post("/{shanyraq_id:str}/comment_shanyraq")
def comment_shanyraq(
    shanyraq_id: str,
    your_comment: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.comment_shanyraq(
        shanyraq_id=shanyraq_id,
        user_id=jwt_data.user_id,
        comment=your_comment,
    )
