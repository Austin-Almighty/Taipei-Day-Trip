from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from config import config

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
		cursor = cnx.cursor()
		cursor.execute("select * from attractions where mrt = %s and name like %s;", (keyword,f"%{keyword}%"))
		results = cursor.fetchall()
	else:
		cursor = cnx.cursor()
		cursor.execute("select * from attractions")
		results = cursor.fetchall()
	
	try:
		start = page*12
		end = (page+1)*12
		spliced_results = results[start:end]
		next_page = page + 1 if end < len(results) else None
		data_list = []

		for item in spliced_results:
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
			data['images'] = item[9]
			data_list.append(data)
			
		response = {"nextPage":next_page, "data":data_list}
		return JSONResponse(response, status_code=200)
		
	except Exception as e:
		return JSONResponse({"error": True, "message": str(e)}, status_code=500)
	