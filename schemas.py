# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# --- USER ---

class CustomerCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name:  str = Field(..., max_length=50)
    adress: int

class CustomerUpdate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = Field(None, max_length=50)
    
class CustomerPatch(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email:    Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    name:  Optional[str] = Field(None, max_length=50)
    
# realtor
class RealtorCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name:  str = Field(..., max_length=50)
    agency: int

class RealtorUpdate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = Field(None, max_length=50)
    agency: int | None
    
# Ads
class AdCreate(BaseModel):
    agreement: str = Field(..., max_length=255)
    customer: int
    publish_date: date
    end_date: date
    realtor: int
    description: str = Field(..., max_length=255)
    price: float
    sold_price:float
    status: str = Field(..., max_length=255)

class AdUpdate(BaseModel):
    agreement: str = Field(..., max_length=255)
    customer: int
    publish_date: date
    end_date: date
    realtor: int
    description: str = Field(..., max_length=255)
    price: float
    sold_price:float
    status: str = Field(..., max_length=255)
# real estate
class RealestateCreate(BaseModel):
    real_estate_type: int
    municipal: int
    adress: int
    living_space: int
    no_of_rooms: int

class RealestateUpdate(BaseModel):
    real_estate_type: int
    municipal: int
    adress: int
    living_space: int
    no_of_rooms: int
    
# review
class RealtorReviewCreate(BaseModel):
    originator: int
    realtor: int
    score: int
    comment: str = Field(..., max_length=255)

class RealtorReviewUpdate(BaseModel):
    originator: int
    realtor: int
    score: int
    comment: str = Field(..., max_length=255)

    
