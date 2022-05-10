from pymongo import MongoClient

mc = MongoClient("mongo")
db = mc["cse312"]
pic_collection = db["pic_location"]

def save_location(name: str):
    path = "images/" + name
    add_path = []
    if (pic_collection.count_documents({}) == 0):
        add_path.append(path)
        pic_collection.insert_one({"path":add_path})
    else:
        retData = pic_collection.find_one({"path":{"$exists":True}})
        print("retDATA value", retData, flush=True)
        old_data = retData["path"]
        old_data.append(path)
        
        pic_collection.replace_one({"path":{"$exists":True}}, {"path":old_data})


def get_id() -> str:
    retData = pic_collection.find_one({"path":{"$exists":True}})
    if retData:
        return str(len(retData["path"]))
    else:
        return "0"