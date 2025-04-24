from fastapi import APIRouter, Query, Path, Depends, Body, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse 
from typing import Annotated, Optional, List, Literal
from pydantic import BaseModel, HttpUrl, EmailStr, Field
import jwt
import os, json
import random
from datetime import datetime, timedelta, timezone, date
from dotenv import load_dotenv
import mysql.connector

from ..database import Database
from ..utilities import *
from ..schemas import *

order_router = APIRouter()
db = Database()
bearer = HTTPBearer()

load_dotenv()
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


# class Attraction(BaseModel):
# 	id: int
# 	name: str
# 	address: str
# 	images: HttpUrl

# class Trip(BaseModel):
# 	attraction: Attraction
# 	date: date
# 	time: Literal["morning", "afternoon"]

# class Contact(BaseModel):
# 	name: str
# 	email: EmailStr
# 	phone: str

# class Order(BaseModel):
# 	price: Literal[2000, 2500]
# 	trip: Trip
# 	contact: Contact
	

# class Payment(BaseModel):
# 	prime: str
# 	order: Order
	

# 建立新的訂單並完成付款
@order_router.post("/api/orders")
async def tap_pay_order(request: Request, payment: Payment, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		token = credentials.credentials
		decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
		userID = decoded_token.get("userID")
		# tappay_prime = payment.get("prime")
		tappay_prime = payment.prime
		# order = payment["order"]
		order = payment.order
		# price = payment["order"]["price"]
		price = order.price
		# date = order["date"]
		date = order.trip.date
		# time = order["time"]
		time = order.trip.time
		# attractionID = payment["order"]['trip']['id']
		attractionID = order.trip.attraction.id
		# contact_name = payment["contact"].get("name")
		contact_name = order.contact.name
		# contact_email = payment["contact"].get("email")
		contact_email = order.contact.email
		# contact_phone = payment["contact"].get("phone")
		contact_phone = order.contact.phone
		status = False
		referenceID = datetime.now().strftime("%Y%m%d%H") + str(random.randint(10000, 99999))
		query = "insert into orders (name, email, phone, attractionID, date, time, price, userID, status, referenceID) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
		para = (contact_name, contact_email, contact_phone, attractionID, date, time, price, userID, status, referenceID)
		db.insert(query, para)
		payload["prime"] = tappay_prime
		payload["amount"] = price
		payload["cardholder"]["phone_number"] = contact_phone
		payload["cardholder"]["name"] = contact_name
		payload["cardholder"]["email"] = contact_email
		# 傳送prime到tappay
		tappay_response = await connect_to_tappay(tappay_URL, headers, payload)
		if not tappay_response:
			return JSONResponse({"error": True, "message": "無法連線到付款服務"}, status_code=400)
		delete_query = "delete from booking where userID = %s;"
		db.insert(delete_query, (userID,))
		if tappay_response["status"] != 0:
			return JSONResponse({"data":{"number": referenceID, "payment":{"status":0, "message":"付款失敗"}}}, status_code=200)
		else:
			update_query = "update orders set status = %s where referenceID = %s;"
			para = (True, referenceID)
			db.insert(update_query, para)
			return JSONResponse({"data":{"number": referenceID, "payment":{"status":1, "message":"付款成功"}}}, status_code=200)
	except jwt.InvalidTokenError:
		return JSONResponse({"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)
	except mysql.connector.Error as e:
		return JSONResponse({"error": True, "message": e}, status_code=400)
	except Exception as e:
		return JSONResponse({"error":True, "message":e}, status_code=500)

# 根據訂單編號取得訂單資訊
@order_router.get("/api/order/{orderNumber}")
def get_order_by_number(request: Request, orderNumber: Annotated[str, Path(title="reference ID created during checkout")], credentials: HTTPAuthorizationCredentials = Depends(bearer)):
	try:
		token = credentials.credentials
		decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
		user_id = decoded_token.get("userID")
		order_query = "select * from orders where referenceID = %s and userID = %s;"
		para = (orderNumber, user_id)
		order_detail = db.select_one(order_query,para)
		if order_detail is None:
			return JSONResponse(None, status_code=200)
		date = order_detail.get("date").isoformat() #Needed to turn the date object into a string, or it will fail the JSONResponse
		time = order_detail.get("time")
		price = order_detail.get("price")
		attractionID = order_detail.get("attractionID")
		contact_name = order_detail.get("name")
		contact_phone = order_detail.get("phone")
		contact_email = order_detail.get("email")
		status = order_detail.get("status")

		attraction_info_query = "select id, name, address, images from attractions where id = %s;"
		attraction_info = db.select_one(attraction_info_query, (attractionID,))

		urls = json.loads(attraction_info["images"])
		first_image = urls[0]
		attraction_info["images"] = first_image
		return JSONResponse({
			"data":{
				"number":orderNumber, 
				"price": price, 
				"trip":{
					"attraction":attraction_info, 
					"date":date, 
					"time": time}
					}, 
				"contact":{
					"name":contact_name, 
					"email":contact_email, 
					"phone":contact_phone},
				"status": status
					}, status_code=200)
	except jwt.InvalidTokenError:
		return JSONResponse({"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)