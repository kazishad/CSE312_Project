from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

def logout_user(username: str) -> None:
    """ Based on username, make db changes: user status and delete their auth token """
    cred_collection.update_one({"username":username}, {"$set":{"user_status":"offline"}}) # TODO: I hope this accesses it correctly
    cred_collection.update_one({"username":username}, {"$set":{"auth_token":None}})