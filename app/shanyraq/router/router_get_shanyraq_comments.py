from fastapi import Depends
from typing import Dict
from ..service import Service, get_service
from . import router
from app.utils import AppModel


class GetCommentsResponse(AppModel):
    comments: Dict


@router.get(
    "/shanyraks/{shanyraq_id:str}/get_comments", response_model=GetCommentsResponse
)
def get_comments(
    shanyraq_id: str,
    svc: Service = Depends(get_service),
):
    resultedComments = svc.repository.get_comments(shanyraq_id=shanyraq_id)

    return GetCommentsResponse(comments=resultedComments)
