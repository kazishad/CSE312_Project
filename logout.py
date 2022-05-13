from pymongo import MongoClient
from authentication import *

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

def logout_user(username: str) -> None:
    # Based on username, make db changes: user status and delete their auth token
    update_status(username, False) # Change status to offline
    change_token(username, "None") # 'delete' auth token (change it to None value)