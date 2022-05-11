from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
pic_collection = db["pic_location"]

def get_id() -> str:
    retData = pic_collection.find_one({"path":{"$exists":True}})
    if retData:
        return str(len(retData["path"]))
    else:
        return "0"

# returns true after adding picture path
# this function can be used to update the location
def picture_location(username: str, image_name: str) -> bool:
    db_return = pic_collection.find_one({"username":username})
    path = "images/" + image_name
    if db_return:
        pic_collection.update_one({"username":username}, {"$set":{"path":path}})
        return True
    else:
        pic_collection.insert_one({"username": username, "path":path})
        return True

# returns the file path, if the account exists, otherwise returns None
def get_path(username: str) -> str:
    db_return = pic_collection.find_one({"username":username})
    if db_return:
        return db_return["path"]
    else:
        return None
