from fastapi import APIRouter, Query, Path, Depends, Body, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse 
from pydantic import BaseModel
import jwt
import os, json
from dotenv import load_dotenv
import mysql.connector

from ..database import Database

load_dotenv()

secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")

booking_router = APIRouter()
db = Database()

bearer = HTTPBearer()

class newBooking(BaseModel):
	attractionID: int
	date: str
	time: str
	price: int

# 取得尚未確認的預定行程
@booking_router.get("/api/booking")
def retrieve_unfinished_booking(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		token = credentials.credentials
		decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
		user_id = decoded_token.get("userID")
		booking_query = "select * from booking where userID = %s;"
		current_booking = db.select_one(booking_query, (user_id,))
		if (current_booking == None):
			return JSONResponse(None)
		date = current_booking.get("date").isoformat() #Needed to turn the date object into a string, or it will fail the JSONResponse
		time = current_booking.get("time")
		price = current_booking.get("price")
		
		attractionID = current_booking["attractionID"]
		attraction_info_query = "select id, name, address, images from attractions where id = %s;"
		attraction_info = db.select_one(attraction_info_query, (attractionID,))
		urls = json.loads(attraction_info["images"])
		first_image = urls[0]
		attraction_info["images"] = first_image
		return JSONResponse({"data":{"attraction":attraction_info, "date": date, "time": time, "price": price}}, status_code=200)
	except jwt.InvalidTokenError:
		return JSONResponse({"error": True, "message":"未登入系統，拒絕存取"}, status_code=403)

# 建立新的預定行程
@booking_router.post("/api/booking")
def create_booking(request: Request, request_body: newBooking, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		attractionID = request_body.attractionID
		date = request_body.date
		time = request_body.time
		price = request_body.price

		token = credentials.credentials
		decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
		user_id = decoded_token.get("userID")

		booking_query = "select * from booking where userID = %s;"
		current_booking = db.select_one(booking_query, (user_id,))

		if current_booking:
			update_query = "update booking set attractionID = %s, date = %s, time = %s, price = %s where userID = %s"
			para = (attractionID, date, time, price, user_id)
			db.insert(update_query, para)
			return JSONResponse({"ok":True}, status_code=200)
		else:
			query = "insert into booking (attractionID, date, time, price, userID) values (%s, %s, %s, %s, %s);"
			para = (attractionID, date, time, price, user_id)
			db.insert(query, para)
			return JSONResponse({"ok": True}, status_code=200)
	except mysql.connector.Error as mysqlerror:
		return JSONResponse({"error": True, "message": str(mysqlerror)}, status_code=400)
	except jwt.InvalidTokenError:
		return JSONResponse({"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)
	except Exception as e:
		return JSONResponse({"error": True, "message": e}, status_code=500)


	

# 刪除目前的預定行程
@booking_router.delete("/api/booking")
def delete_booking(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try: 
		token = credentials.credentials
		decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
		user_id = decoded_token.get("userID")

		query = "delete from booking where userID = %s;"
		db.insert(query, (user_id,))
		return JSONResponse({"ok": True})
	except jwt.InvalidTokenError:
		return JSONResponse({"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)
	