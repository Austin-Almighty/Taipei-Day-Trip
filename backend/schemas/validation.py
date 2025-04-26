from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, List, Literal
from datetime import date

#attractions.py
class AttractionFull(BaseModel):
	id: int
	name: str
	category: str
	description: str
	address: str
	transport: str
	mrt: Optional[str] = None
	lat: float
	lng: float
	images: List[HttpUrl]

class AttractionsResponse(BaseModel):
	nextPage: Optional[int]
	data: List[AttractionFull]

class AttractionResponse(BaseModel):
	data: AttractionFull

class MrtResponse(BaseModel):
	data: List[str]

#user.py
class NewUser(BaseModel):
	name: str
	email: EmailStr
	password: str

class LoginPayload(BaseModel):
	email: EmailStr
	password: str

#booking.py
class newBooking(BaseModel):
	attractionID: int
	date: str
	time: Literal["morning", "afternoon"]
	price: Literal[2000, 2500]

#orders.py
class Attraction(BaseModel):
	id: int
	name: str
	address: str
	images: HttpUrl

class Trip(BaseModel):
	attraction: Attraction
	date: date
	time: Literal["morning", "afternoon"]

class Contact(BaseModel):
	name: str
	email: EmailStr
	phone: str

class Order(BaseModel):
	price: Literal[2000, 2500]
	trip: Trip
	contact: Contact
	

class Payment(BaseModel):
	prime: str
	order: Order