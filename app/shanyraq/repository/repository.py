from datetime import datetime
from typing import List
from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult


class ShanyraqRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_comments(self, shanyraq_id) -> List[dict]:
        comments = self.database["comments"].find_one(
            {"shanyraq_id": ObjectId(shanyraq_id)}
        )
        comments.pop("_id")
        return comments

    def comment_shanyraq(self, shanyraq_id: str, user_id: str, comment: str):
        com = self.database["comments"].update_one(
            filter={"shanyraq_id": ObjectId(shanyraq_id)},
            update={"$push": {user_id: comment}},
        )
        print(com.inserted_id)

    def delete_file(self, user_id, shanyraq_id, url):
        shanyraq = self.database["shanyraqs"].find_one(
            {
                "_id": ObjectId(shanyraq_id),
                "user_id": ObjectId(user_id),
            }
        )
        if url in shanyraq["media"]:
            shanyraq["media"].remove(url)
        else:
            raise HTTPException(status_code=404)

        self.database["shanyraqs"].update_one(
            filter={
                "_id": ObjectId(shanyraq_id),
                "user_id": ObjectId(user_id),
            },
            update={"$set": shanyraq},
        )

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
        self.database["comments"].insert_one({"shanyraq_id": res.inserted_id})
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
