from pymongo import MongoClient # Let your server talk to MongoDB
from collections import ChainMap
import secrets

mc = MongoClient("mongo")
db = mc["cse312"]
xsrf_token_storage = db["xsrf_tokens"]


def print_xsrf_tokens():
    tokens = get_xsrf_tokens()
    print(f"==> (called print()) tokens was {tokens}", flush=True)


def generate_xsrf_token() -> str:
    """ Returns a xsrf_token as string and stores it (persistant) in our db """
    # Generate XSRF token and embed into the html
    xsrf_token = secrets.token_urlsafe(10) # length of 10, as string
    xsrf_token_storage.insert_one({xsrf_token: 0}) # Store token in db
    print_xsrf_tokens()
    return xsrf_token
        

def get_xsrf_tokens() -> list:
    stored_xsrf_tokens = xsrf_token_storage.find({}, {"_id": 0}) # Obtain all the tokens (remember they are in dictionary form)
    # print(f"first tokens: {stored_xsrf_tokens}", flush=True)
    list_of_tokens = list(stored_xsrf_tokens)
    # print(f"==> stored_xsrf_tokens was: {list_of_tokens}", flush=True)
    stored_xsrf_tokens_list = list_of_tokens # Create iterable for for-loop
    # print(f">stored_xsrf_tokens_list: {stored_xsrf_tokens_list}", flush=True)
    stored_xsrf_tokens_dict = ChainMap(*stored_xsrf_tokens_list) # Flatten list of dicts to --> list
    print(stored_xsrf_tokens_dict, flush=True)
    keys = list(stored_xsrf_tokens_dict.keys()) # The tokens are stored in the keys of the dict
    return keys


def validate_xsrf_token(xsrf_token: str) -> bool:
    """ Returns boolean: True if valid token | False if not found """
    
    xsrf_tokens = get_xsrf_tokens()
    print(f"\n==> xsrf_tokens was {xsrf_tokens}", flush=True)
    for stored_xsrf_token in xsrf_tokens: # The tokens themselves are stored in the keys
        if xsrf_token == stored_xsrf_token:
            return True

    return False # Return False if we did not find a match


def custom_render_template(filename_dir: str, placeholder: str, replace_with: str) -> str:
    """
    Replaces one instance (the first) placeholder

    filename_dir: the filename pathed from the root (example: "templates/upload_image.html")
    placeholder: the thing inside the {{}} that we are replacing
    replace_with: what we are replacing the placeholder with

    returns: html file as a string, with replacement
    """

    with open(filename_dir) as f:
        html = f.read()
    html = html.replace("{{"+placeholder+"}}", replace_with)
    return html