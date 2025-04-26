from fastapi import APIRouter, Query, Path, Depends, Body
from fastapi.responses import JSONResponse
from typing import Annotated, List, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError, ResponseValidationError
import argon2
from argon2 import PasswordHasher
import jwt
import mysql.connector
from mysql.connector import Error
import os, json
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from fastapi import Request
from ..database import *
from ..schemas import *

load_dotenv()
secret_key = os.getenv('secret_key')
algorithm = os.getenv('algorithm')



user_router = APIRouter()
db = shared_pool
ph = PasswordHasher()
bearer = HTTPBearer()

# class NewUser(BaseModel):
# 	name: str
# 	email: EmailStr
# 	password: str

# class LoginPayload(BaseModel):
# 	email: EmailStr
# 	password: str

# 註冊一個新的會員
@user_router.post("/api/user")
def signup(request: Request, new_user: NewUser):
	try:
		name = new_user.name
		email = new_user.email
		password = new_user.password
		hashed_password = ph.hash(password)
		query = "insert into users (name, email, password) values (%s, %s, %s);"
		para = (name, email, hashed_password)
		db.insert(query, para)
		return JSONResponse({"ok": True}, status_code=200)
	except mysql.connector.IntegrityError as e:
		if e.errno == 1062:
			return JSONResponse({"error": True, "message": "此Email已被註冊過了"}, status_code=400)
		return JSONResponse({"error":True, "message":"註冊失敗"}, status_code=400)
	except Exception as e:
		return JSONResponse({"error":True, "message":"伺服器內部錯誤"}, status_code=500)
	except RequestValidationError:
		return JSONResponse({"error": True, "message":"請輸入有效的email地址"}, status_code=422)



# 取得當前的用戶資訊

@user_router.get("/api/user/auth")
def fetch_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		token = credentials.credentials
		payload = jwt.decode(token, secret_key, algorithms=algorithm)
		user_data = {
			"id":payload.get("userID"),
			"name": payload.get("name"),
			"email": payload.get("email")
		}
		# query = "select * from users where userID = %s and name = %s and email = %s;"
		# para = (id)
		return JSONResponse({"data":user_data}, status_code=200)
	except jwt.InvalidTokenError:
		return JSONResponse(None, status_code=200)
	
# 登入會員帳戶
@user_router.put("/api/user/auth")
def login(request: Request, login_payload: LoginPayload):
	try:
		email = login_payload.email
		password = login_payload.password
		query = "select * from users where email = %s;"
		para = (email,)
		result = db.select_one(query, para)
		if result is None:
			return JSONResponse({"error": True, "message": "登入失敗，帳號或密碼錯誤"}, status_code=400)
		hash_db = result['password']

		if ph.verify(hash_db, password):
			expiration_time = datetime.now(tz=timezone.utc) + timedelta(days=7)
			result["exp"] = expiration_time
			encoded = jwt.encode(result, secret_key, algorithm=algorithm)
			return JSONResponse({"token": encoded}, status_code=200)
		
	except argon2.exceptions.VerifyMismatchError:
			return JSONResponse({"error": True, "message": "登入失敗，帳號或密碼錯誤"}, status_code=400)
	except Exception as e:
		return JSONResponse({"error": True, "message": e}, status_code=500)
	except RequestValidationError:
		return JSONResponse({"error": True, "message":"請輸入有效的email地址"}, status_code=422)