import hashlib
from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

def create(username: str, password: str) -> str:
    # implement salt here
    hashed_pass = hashlib.sha512(password.encode()).hexdigest()
    cred_collection.insert_one({"username": username, "password":hashed_pass})
    return "account created for " + username

def verify(username: str, password: str) -> bool:
    # search db to find hash
    db_return = cred_collection.find_one({"username": username})
    if db_return:
        hashed_pass = db_return["password"]
        current_hash = hashlib.sha512(password.encode()).hexdigest()
        if (hashed_pass == current_hash):
            print("identity verified for", username)
            return True
        else:
            print("wrong password or email for ", username)
            return False
    else:
        print("username does not exist")
        return False