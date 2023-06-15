from fastapi import Depends, Response
from typing import List
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/{shanyraq_id:str}/deleteFiles")
def delete_files(
    shanyraq_id: str,
    media: List[str],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    for url in media:
        svc.repository.delete_file(
            user_id=jwt_data.user_id,
            shanyraq_id=shanyraq_id,
            url=url
        )
        svc.s3_service.delete_file(url)
    
        
            