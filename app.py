from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routers import *

app=FastAPI()

app.mount("/css", StaticFiles(directory="frontend/CSS"), name="css")
app.mount("/js",  StaticFiles(directory="frontend/js"), name="js")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/static", StaticFiles(directory="frontend/static", html=True), name="static")

app.include_router(attraction_router)
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(order_router)

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./frontend/static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./frontend/static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./frontend/static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./frontend/static/thankyou.html", media_type="text/html")


