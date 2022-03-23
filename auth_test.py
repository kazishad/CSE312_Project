import authentication

# creating accounts
authentication.create("David","123")
authentication.create("Alex", "password")
authentication.create("Maria", "qwerty")

# verifying users
authentication.verify("David", "123")
authentication.verify("Alex", "password")
authentication.verify("Maria", "qwerty")

# non-existent account
authentication.verify("Anna", "qwerty123")