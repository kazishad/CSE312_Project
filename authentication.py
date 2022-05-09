import bcrypt
from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

def create(username: str, password: str) -> bool:
    b_pass = password.encode()
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(b_pass,salt)

    cred_collection.insert_one({"username": username, "password":hashed_pass, "pic_path":"None"})
    return True

# returns true if the account exists and has been verified, false if the password or username is wrong,
# or if the account could not be found
def verify(username: str, password: str) -> bool:
    b_pass = password.encode()
    db_return = cred_collection.find_one({"username": username})
    if db_return:
        db_hashed_pass = db_return["password"]
        return bcrypt.checkpw(b_pass, db_hashed_pass)
    else:
        return False

# returns true of the pic path was changed, false if the account could not be found
def change_prof_pic(username:str, old_path: str, new_path: str) -> bool:
    db_return = cred_collection.find({"username":username})
    if db_return:
        cred_collection.update_one({"pic_path":old_path}, {"$set":{"pic_path":new_path}})
        return True
    else:
        return False

