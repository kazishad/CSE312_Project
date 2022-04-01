import authentication

# example of calling the create function
# authentication.create("David","123")
# authentication.create("Alex", "password")
# authentication.create("Maria", "qwerty")

# example of calling the verify function 
# authentication.verify("David", "123")
# authentication.verify("Alex", "password")
# authentication.verify("Maria", "qwerty")


# Input is a dictionary in [{"username":<username>,"password":<password>}] format
def create_multi_account(data:list):
    for info in data:
        if authentication.create(info["username"], info["password"]):
            print("account created for", info["username"])
        else:
            print("error in creating account for", info["username"])
    

# Input is a dictionary in [{"username":<username>,"password":<password>}] format
def verify_multi_account(data: list):
    for info in data:
        if authentication.verify(info["username"], info["password"]):
            print("user", info["username"], "has been verified")
        else:
            print("user", info["username"], "could not be verified")


# create_and_verify only exists because we are lazy lol
def create_and_verify(data: list):
    create_multi_account(data)
    verify_multi_account(data)

# creating multiple accounts
account_info = [{"username":"David", "password":"123"}, 
                {"username":"Alex", "password":"password"}, 
                {"username":"Maria", "password":"qwerty"},
                {"username":"Anna", "password": "12345678"},
                {"username":"Maro", "password": "1q2w3e"}]

create_and_verify(account_info)
        