from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Annotated, List, Optional
from .attractions import *
from fastapi import Request
from ..database import *


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
	data: Attraction

class MrtResponse(BaseModel):
	data: List[str]

attraction_router = APIRouter()
db = Database()

@attraction_router.get('/api/attractions', response_model=AttractionsResponse)
async def find_attractions(request: Request, page: Annotated[int, Query()], keyword: Annotated[str | None, Query(max_length=20)] = None):
	try:
		limit = 13
		offset = page*12
		if keyword:
			query= "select * from attractions where mrt = %s or name like %s limit %s offset %s;"
			para = (keyword, f"%{keyword}%", limit, offset)
			results = db.select_all(query, para)
		else:
			query = "select * from attractions limit %s offset %s;"
			para = (limit, offset)
			results = db.select_all(query, para)

		next_page = page + 1 if len(results) == limit else None
		if len(results) == 13:
			data_list = [result for result in results[:-1]]
		else:
			data_list = [result for result in results]
		
		return JSONResponse({"nextPage": next_page, "data":data_list}, status_code=200)
	except Exception as e:
		print(str(e))
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)
	

@attraction_router.get("/api/attraction/{attractionID}", response_model=AttractionResponse)
async def one_attraction(request: Request, attractionID: Annotated[int, Path()]):
	try:
		query = "select * from attractions where id = %s;"
		para = (attractionID,)
		results = db.select_one(query, para)

		if results is None:
			return JSONResponse({"error": True, "message": "景點編號不正確"}, status_code=400)
		return JSONResponse({"data":results}, status_code=200)
	
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)

@attraction_router.get('/api/mrts', response_model=MrtResponse)
async def mrts(request: Request):
	try:
		# cursor.execute("select mrt from attractions group by mrt order by count(mrt) desc")
		# stations = cursor.fetchall()
		# data = [station[0] for station in stations if station[0]]
		query = "select mrt from attractions group by mrt order by count(mrt) desc;"
		results = db.select_all(query)
		return JSONResponse({"data":results}, status_code=200)
	except Exception:
		return JSONResponse({"error": True, "message": "伺服器內部錯誤"}, status_code=500)
