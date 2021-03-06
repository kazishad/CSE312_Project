from authentication import create, verify, auth_token, user_list, online_now, update_status, username_from_auth_token, change_token
import save_picture

print(create("user1","password1"), flush=True)

print(create("user2","password2"), flush=True)

print(create("user1","password2"), flush=True)


# Auth_Token Test

retVal = auth_token("user1", "password1")
print(f"auth_token for user1: {retVal}", flush=True)


retVal = auth_token("user3", "password3")
print(f"auth_token for user2: {retVal}", flush=True)



print(user_list(), flush=True)

create("user3", "password3")
update = update_status("user1", False)

print(f"updated value? {update}", flush=True)

print(online_now(), flush=True)

temp, user3_auth = auth_token("user3","password3")

username = username_from_auth_token(user3_auth)
print(f"auth username{username}", flush=True)


print(change_token("user1","987yughbjhiijlk"), flush=True)

print(change_token("user5","0987uyghjbn"), flush=True)

print(save_picture.get_id())
save_picture.picture_location("user7","picture0.jpg")


print(save_picture.get_id())
save_picture.picture_location("user8","picture1.jpg")
print(save_picture.get_id())
