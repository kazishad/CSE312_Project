from pymongo import MongoClient # Let your server talk to MongoDB
from collections import ChainMap
import secrets

mc = MongoClient("mongo")
db = mc["cse312"]
xsrf_token_storage = db["xsrf_tokens"]

def generate_xsrf_token() -> str:
    """ Returns a xsrf_token as string and stores it (persistant) in our db """
    # Generate XSRF token and embed into the html
    xsrf_token = secrets.token_urlsafe(10) # length of 10, as string
    xsrf_token_storage.insert_one({xsrf_token: 0}) # Store token in db
    return xsrf_token
        

def validate_xsrf_token(xsrf_token) -> bool:
    """ Returns boolean: True if valid token | False if not found """

    stored_xsrf_tokens = xsrf_token_storage.find({}, {"_id": 0}) # Obtain all the tokens (remember they are in dictionary form)
    stored_xsrf_tokens_list = list(stored_xsrf_tokens) # Create iterable for for-loop

    stored_xsrf_tokens_dict = ChainMap(*stored_xsrf_tokens_list) # Flatten list of dicts to --> list
    for stored_xsrf_token in stored_xsrf_tokens_dict.keys(): # The tokens themselves are stored in the keys
        if xsrf_token == stored_xsrf_token:
            return True

    return False # Return False if we did not find a match
