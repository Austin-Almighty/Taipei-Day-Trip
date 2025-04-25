from fastapi import APIRouter, Request, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
import jwt
from dotenv import load_dotenv
import os

from ..database import shared_pool

load_dotenv()
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")

member_router = APIRouter()

db = shared_pool
bearer = HTTPBearer()

@member_router.get("/api/member")
def retrieve_member(request: Request, login: Annotated[dict, Body()], credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
    email = login.get("email")
    password = login.get("password")
    retrieve_query = "select userID, name, email from users where email = %s;"

    return

# @member_router.put("/api/member")

# Design your own user interface and APIs for the features on the member page:
# a. Features for member profile updates: name and email.
# b. Features for member picture uploading.
# c. Historical order list where a member can click to view order details