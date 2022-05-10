import pymongo
myclient = pymongo.MongoClient("mongo")

mydb = myclient["mydatabase"]
my_user_data = mydb["user_data"]
def create_new_user( username, password):
    adict = {"username": username , "password": password, "stat": "offline", }
    my_user_data.insert_one(adict)
    pass


def login_check(username, password):
    result = my_user_data.find_one({"username": username , "password": password})
    print(result)
    return result
