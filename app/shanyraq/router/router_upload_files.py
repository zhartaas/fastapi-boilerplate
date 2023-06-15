from fastapi import Depends, Response, UploadFile
from typing import List
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data



@router.post("/{shanyraq_id:str}/upload")
def upload_files(
    files: List[UploadFile],
    shanyraq_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, List]:
    
    media = []

    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        media.append(url)

    svc.repository.insert_media(jwt_data.user_id, shanyraq_id, media)

    return {"media" : media}
