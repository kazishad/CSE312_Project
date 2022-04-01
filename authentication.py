import bcrypt
from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

def create(username: str, password: str) -> bool:
    b_pass = password.encode()
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(b_pass,salt)

    cred_collection.insert_one({"username": username, "password":hashed_pass})
    return True


def verify(username: str, password: str):
    b_pass = password.encode()
    db_return = db_return = cred_collection.find_one({"username": username})
    if db_return:
        db_hashed_pass = db_return["password"]
        return bcrypt.checkpw(b_pass, db_hashed_pass)
    else:
        return False
