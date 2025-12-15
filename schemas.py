# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# --- USER ---

class CustomerCreate(BaseModel):
    type: int
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name:  str = Field(..., max_length=50)

class CustomerUpdate(BaseModel):
    type: int
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = Field(None, max_length=50)
    
class CustomerPatch(BaseModel):
    type: Optional[int] = None
    username: Optional[str] = Field(None, max_length=50)
    email:    Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    name:  Optional[str] = Field(None, max_length=50)
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
    type: int
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = Field(None, max_length=50)
    
