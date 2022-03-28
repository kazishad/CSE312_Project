# Account creation and Authentication

The authentication system has two functions, the first is creating an account, and the second is verifying the user's identity. It creates the account by taking in the username and password on its `create()` function, hashing the password, and saving it on the database. The function returns `True` to state the account was created. Salting for the password will be implemented later. It verifies the account by taking in the username and password on its `verify()` function, getting the username and hashed password from the database, hasing the given password and comparing them.

When a new account is created the `create()` function returns `True` indicating that the account was created. The `verify()` function returns `True` if the username and password matches the with existing account on the database and `False` otherwise.

The usernames and passwords are case-sensitive.

## Testing Guide
The `auth_test.py` file contains the sample test. Feel free to add to it to try and break things :) <br>
Create an issue if there are any problems or if the service isn't working as intended.

To test the authentication service:
1. Clone the branch using `git clone -b authentication https://github.com/kazishad/CSE312_Project.git`
2. Run the docker file using `docker-compose up --build`
3. The terminal should print which accounts were created
4. It should also print whether the accounts were verified or not
