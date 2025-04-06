from fastapi import FastAPI, Request, Query, Body, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from typing import Annotated, List, Optional
from config import config
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
from key import secret_key, algorithm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import argon2
from argon2 import PasswordHasher

cnx = mysql.connector.connect(**config)

app=FastAPI()

app.mount("/external", StaticFiles(directory="external"), name="external")
templates = Jinja2Templates(directory="static")

ph = PasswordHasher()

class Attraction(BaseModel):
	id: int
	name: str
	category: str
	description: str
	address: str
	transport: str
	mrt: Optional[str] = None
	lat: float
	lng: float
	images: List[str]

class AttractionsResponse(BaseModel):
	nextPage: Optional[int]
	data: List[Attraction]

class AttractionResponse(BaseModel):
	data: List[Attraction]

class MrtResponse(BaseModel):
	data: List[str]

# class 

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

@app.get('/api/attractions', response_model=AttractionsResponse)
async def find_attractions(request: Request, page: int = Query(), keyword: str = Query(default=None)) :
	if keyword:
		limit = 13
		offset = page*12
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("select * from attractions where mrt = %s or name like %s limit %s offset %s;", (keyword,f"%{keyword}%", limit, offset))
		results = cursor.fetchall()
	else:
		limit = 13
		offset = page*12
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("select * from attractions limit %s offset %s;", (limit, offset))
		results = cursor.fetchall()
	
	try:
		next_page = page + 1 if len(results) == limit else None
		if len(results) == 13:
			data_list = [result for result in results[:-1]]
		else:
			data_list = [result for result in results]
			
		response = {"nextPage":next_page, "data":data_list}
		return JSONResponse(response, status_code=200)
		
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

@app.get("/api/attraction/{attractionID}", response_model=AttractionResponse)
async def one_attraction(request: Request, attractionID: int):
	try:
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("select * from attractions where id = %s;", (attractionID,))
		result = cursor.fetchone()

		if result is None:
			return JSONResponse({"error": True, "message": "景點編號不正確"}, status_code=400)

		return JSONResponse({"data":result}, status_code=200)
	
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

@app.get('/api/mrts', response_model=MrtResponse)
async def mrts(request: Request):
	try:
		cursor = cnx.cursor()
		cursor.execute("select mrt from attractions group by mrt order by count(mrt) desc")
		stations = cursor.fetchall()
		data = [station[0] for station in stations if station[0]]
		return JSONResponse({"data":data}, status_code=200)
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

# 註冊一個新的會員
@app.post("/api/user")
def signup(request: Request, payload: Annotated[dict, Body()]):
	try:
		name = payload.get("name")
		email = payload.get("email")
		password = payload.get("password")
		hashed_password = ph.hash(password)
		query = "insert into users (name, email, password) values (%s, %s, %s);"
		cursor = cnx.cursor(dictionary=True)
		cursor.execute(query, (name, email, hashed_password))
		cnx.commit()
		return JSONResponse({"ok": True}, status_code=200)
	except mysql.connector.IntegrityError as e:
		if e.errno == 1062:
			return JSONResponse({"error": True, "message": "此Email已被註冊過了"}, status_code=400)
		return JSONResponse({"error":True, "message":"註冊失敗"}, status_code=400)
	except Exception as e:
		return JSONResponse({"error":True, "message":"伺服器內部錯誤"}, status_code=500)



# 取得當前的用戶資訊
bearer = HTTPBearer()
@app.get("/api/user/auth")
def fetch_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		token = credentials.credentials
		payload = jwt.decode(token, secret_key, algorithms=algorithm)
		user_data = {
			"id":payload.get("userID"),
			"name": payload.get("name"),
			"email": payload.get("email")
		}
		return JSONResponse({"data":user_data}, status_code=200)
	except jwt.InvalidTokenError:
		return JSONResponse(None, status_code=200)
# 登入會員帳戶
@app.put("/api/user/auth")
def login(request: Request, payload: Annotated[dict, Body()]):
	try:
		email = payload.get("email")
		password = payload.get("password")
		query = "select * from users where email = %s;"
		cursor = cnx.cursor(dictionary=True)
		cursor.execute(query,(email,))
		result = cursor.fetchone() 
		hash_db = result['password']

		if ph.verify(hash_db, password):
			expiration_time = datetime.now(tz=timezone.utc) + timedelta(days=7)
			result["exp"] = expiration_time
			encoded = jwt.encode(result, secret_key, algorithm=algorithm)
			return JSONResponse({"token": encoded}, status_code=200)
		elif not result:
			return JSONResponse({"error": True, "message": "登入失敗，帳號或密碼錯誤"}, status_code=400)
	except argon2.exceptions.VerifyMismatchError:
			return JSONResponse({"error": True, "message": "登入失敗，帳號或密碼錯誤"}, status_code=400)
	except Exception as e:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

