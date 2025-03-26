from utils.jwt_utils import create_access_token

data = {"username":"gogagoga", "password":"gogagoga"}
token = create_access_token(data)

print("Token: ", token)

