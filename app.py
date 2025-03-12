from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from config import config
import json

cnx = mysql.connector.connect(**config)

app=FastAPI()

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

@app.get('/api/attractions')
async def find_attractions(request: Request, page: int = Query(), keyword: str = Query(default=None)) :
	if keyword:
		offset = page*12
		cursor = cnx.cursor()
		cursor.execute("select * from attractions where mrt = %s or name like %s limit 12 offset %s;", (keyword,f"%{keyword}%", offset))
		results = cursor.fetchall()
	else:
		offset = page*12
		cursor = cnx.cursor()
		cursor.execute("select * from attractions limit 12 offset %s;", (offset,))
		results = cursor.fetchall()
	
	try:
		next_page = page + 1
		data_list = []

		for item in results:
			data = {}
			data['id'] = item[0]
			data['name'] = item[1]
			data['category'] = item[2]
			data['description'] = item[3]
			data['address'] = item[4]
			data['transport'] = item[5]
			data['mrt'] = item[6]
			data['lat'] = item[7]
			data['lng'] = item[8]
			data['images'] = json.loads(item[9])
			data_list.append(data)
			
		response = {"nextPage":next_page, "data":data_list}
		return JSONResponse(response, status_code=200)
		
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

@app.get("/api/attraction/{attractionID}")
async def one_attraction(request: Request, attractionID: int):
	try:
		cursor = cnx.cursor()
		cursor.execute("select * from attractions where id = %s;", (attractionID,))
		result = cursor.fetchone()

		if result is None:
			return JSONResponse({"error": True, "message": "景點編號不正確"}, status_code=400)

		data = {
            "id": result[0],
            "name": result[1],
            "category": result[2],
            "description": result[3],
            "address": result[4],
            "transport": result[5],
            "mrt": result[6],
            "lat": result[7],
            "lng": result[8],
            "images": json.loads(result[9])
        }
		return JSONResponse({"data":data}, status_code=200)
	
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

@app.get('/api/mrts')
async def mrts(request: Request):
	try:
		cursor = cnx.cursor()
		cursor.execute("select mrt from attractions group by mrt order by count(mrt) desc")
		stations = cursor.fetchall()
		data = [station[0] for station in stations if station[0]]
		return JSONResponse({"data":data}, status_code=200)
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)
