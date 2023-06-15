from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult


class ShanyraqRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyraq(self, user_id: str, data: dict):
        payload = {
            "user_id": ObjectId(user_id),
            "type": data["type"],
            "price": data["price"],
            "address": data["address"],
            "area": data["area"],
            "rooms_count": data["rooms_count"],
            "description": data["description"],
            "created_at": datetime.utcnow(),
        }

        res = self.database["shanyraqs"].insert_one(payload)
        return res.inserted_id

    def delete_shanyraq(self, user_id: str, shanyraq_id: str) -> DeleteResult:
        return self.database["shanyraqs"].delete_one(
            {
                "_id": ObjectId(shanyraq_id),
                "user_id": ObjectId(user_id),
            }
        )

    def get_my_shanyraq_by_id(self, user_id: str) -> List[dict]:
        shanyraqs = self.database["shanyraqs"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []
        for shanyraq in shanyraqs:
            result.append(shanyraq)

        return result

    def update_shanyraq(self, user_id: str, shanyraq_id: str, data: dict):
        self.database["shanyraqs"].update_one(
            filter={
                "_id": ObjectId(shanyraq_id),
                "user_id": ObjectId(user_id),
            },
            update={"$set": data},
        )

    def insert_media(self, user_id: str, shanyraq_id, urls: List):
        shanyraq = self.database["shanyraqs"].find_one(
            {
                "_id": ObjectId(shanyraq_id),
                "user_id": ObjectId(user_id),
            }
        )
        if "media" in shanyraq:
            shanyraq["media"].extend(urls)
        else:
            shanyraq["media"] = urls

        self.update_shanyraq(user_id, shanyraq_id, shanyraq)