## Report
The report is in the folder labeled `reports`, alternatively [click here](https://drive.google.com/drive/folders/1nhWZlB2AqQzha-IXWn8WPgfKEPMN_UT6?usp=sharing)

## About Application and how to use

We developed an anonymous chat platform.
You can login at /login, register for an account at /register, homepage is at /, visit any profile by going to /&lt;username&gt;
The chat at /chat works by adding an anonymous username and picking a topic (the other user has to have the same topic, exactly)
Live interaction is upvoting DMs, which you can click on (click again to un-upvote) and it will turn blue to indicate that it has been upvoted

## Team Members

| Names          |    UBIT    |       Github Email        |
| -------------- | :--------: | :-----------------------: |
| Kazi Shadman   | `kazishad` |  `kazishad@buffalo.edu`   |
| Shkar Bassam   | `mbassam`  |   `mbassam@buffalo.edu`   |
| Aleena Sheikh  | `aleenash` | `aleenabsheikh@gmail.com` |
| Kevin Wang     | `kwang47`  |   `kwang47@buffalo.edu`   |
| Wren Martinson | `wrenmart` |  `wrenmart@buffalo.edu`   |

# Account creation and Authentication

The authentication system has two functions, the first is creating an account, and the second is verifying the user's identity. It creates the account by taking in the username and password on its `create()` function, generating a salt, hashing the password using the salt, and saving it on the database. The function returns `True` to state the account was created. It verifies the account by taking in the username and password on its `verify()` function, getting the username and hashed password from the database, encoding the given password and comparing them.

When a new account is created the `create()` function returns `True` indicating that the account was created. The `verify()` function returns `True` if the username and password matches the with existing account on the database and `False` otherwise.

The usernames and passwords are case-sensitive.

## Resources

[Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/) <br>
[Flask Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/) <br>
[Tutorial Point: Flask](https://www.tutorialspoint.com/flask/flask_overview.htm) <br>

## To run Flask App

```
FLASK_ENV=development flask run
```

## Testing Guide

The `auth_test.py` file contains the sample test. Feel free to add to it to try and break things :) <br>
Create an issue if there are any problems or if the service isn't working as intended.

To test the authentication service:

1. Clone the branch using `git clone -b dev https://github.com/kazishad/CSE312_Project.git`
2. Run the docker file using `docker-compose up --build`
