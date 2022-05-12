import secrets
import hashlib
import bcrypt
from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
cred_collection = db["credentials"]

# returns true if the account was created
# returns false if accounts with the same username exists
def create(username: str, password: str) -> bool:
    db_return = cred_collection.find_one({"username":username})
    if db_return:
        return False
    else:
        b_pass = password.encode()
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(b_pass,salt)

        cred_collection.insert_one({"username": username, "password":hashed_pass, "pic_path":"None", "status":True})
        return True

# returns true if the account exists and has been verified, false if the password or username is wrong,
# or if the account could not be found
def verify(username: str, password: str) -> bool:
    b_pass = password.encode()
    db_return = cred_collection.find_one({"username": username})
    if db_return:
        db_hashed_pass = db_return["password"]
        cred_collection.update_one({"username":username}, {"$set":{"status":True}})
        return bcrypt.checkpw(b_pass, db_hashed_pass)
    else:
        return False

# returns true of the pic path was changed, false if the account could not be found
def change_prof_pic(username: str, new_path: str) -> bool:
    db_return = cred_collection.find({"username":username})
    if db_return:
        cred_collection.update_one({"username":username}, {"$set":{"pic_path":new_path}})
        return True
    else:
        return False

# updates status to input value, return false if status could not be updated 
# or the account could not be found
def update_status(username: str, status: bool) -> bool:
    db_return = cred_collection.find_one({"username":username})
    if db_return:
        cred_collection.update_one({"username":username}, {"$set":{"status":status}})
        return True
    else:
        return False

# returns a tuple, values would either be (True, <auth_token>) or (False, None), 
# May return (False, None) if either username and/or password are wrong or if the account does not exist
def auth_token(username: str, password: str) -> tuple:
    if verify(username, password):
        auth_token = secrets.token_urlsafe(30)
        hashed_token = hashlib.sha256(auth_token.encode()).hexdigest()
        cred_collection.update_one({"username":username}, {"$set":{"auth_token":hashed_token}})
        return (True, auth_token)
    else:
        return (False, None)

# returns a list of names of all the accounts created
# returns an empty list if there aren't anything
def user_list() -> list:
    db_return = cred_collection.find({})
    retList = []
    if db_return:
        for data in db_return:
            retList.append(data["username"])
    return retList

def check_user(username) -> bool:
    db_return = cred_collection.find({"username": username})
    retList = []
    if db_return:
        return True
    else:
        return False

# returns list of users that has True for status on the database
# returns an empty list if there aren't any others
def online_now() -> list:
    db_return = cred_collection.find({"status":True})
    retList = []
    if db_return:
        for data in db_return:
            retList.append(data["username"])
    return retList

# returns the a tuple (True, <username>) if the account was found
# or (False, None) if there are no accounts with the same auth_token could not be found
def username_from_auth_token(token: str) -> tuple:
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    db_return = cred_collection.find_one({"auth_token":hashed_token})
    if db_return:
        return db_return["username"]
    else:
        return None

# returns true if the token has been updated
# returns false if the account could not be found
def change_token(username: str, new_token: str) -> bool:
    db_return = cred_collection.find_one({"username":username})
    hashed_token = hashlib.sha256(new_token.encode()).hexdigest()
    if db_return:
        cred_collection.update_one({"username":username}, {"$set":{"auth_token":hashed_token}})
        return True
    else:
        return False

