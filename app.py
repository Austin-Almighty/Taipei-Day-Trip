from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
from typing import Annotated, List, Optional
from starlette.middleware.sessions import SessionMiddleware
from config import config
from pydantic import BaseModel

cnx = mysql.connector.connect(**config)

app=FastAPI()

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
		data_list = [result for result in results[:-1]]
			
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
