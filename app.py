import os

import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from db import get_all_customers_db, get_customer_db, add_customer_db, delete_customer_db, patch_customer_db, update_customer_db
from db import get_all_ads_db, get_ad_db, add_ad_db, delete_ad_db, update_ad_db
from db import  add_realtor_db, delete_realtor_db, update_realtor_db 
from db import  add_real_estate_db, delete_real_estate_db, update_real_estate_db 
from db import  add_realtor_review_db, delete_realtor_review_db, update_realtor_review_db, get_all_realtor_reviews_db 
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from schemas import (
    CustomerCreate, CustomerUpdate,CustomerPatch,
    AdCreate, AdUpdate,
    RealtorCreate, RealtorUpdate,
    RealestateCreate, RealestateUpdate,
        RealtorReviewCreate, RealtorReviewUpdate
)
from psycopg2 import errors
from psycopg2 import sql

app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values


@app.get("/customers/")
def get_all_customers(limit: int=20):
    """ Return all customers"""
    con = get_connection()
    customers = get_all_customers_db(con,limit)
    return {"customers": customers}

@app.get("/customers/{customer_id}")
def get_customer(customer_id):
    """Return customer info"""
    con = get_connection()
    try:
        customer = get_customer_db(con,customer_id)
        return {"customer": customer}
    except ValueError:
        raise HTTPException(status_code=404, detail="customer not found")
@app.get("/ads/")
def get_all_ads(limit: int=20):
    """ Return all customers"""
    con = get_connection()
    ads = get_all_ads_db(con,limit)
    return {"ads": ads}

@app.get("/ads/{ad_id}")
def get_ad(ad_id):
    """Return customer info"""
    con = get_connection()
    try:
        ad = get_ad_db(con,ad_id)
        return {"ad": ad}
    except ValueError:
        raise HTTPException(status_code=404, detail="ad not found")
@app.get("/realtor_reviews/")
def get_all_realtor_reviews(limit: int=20):
    """ Return all reviews"""
    con = get_connection()
    customers = get_all_realtor_reviews_db(con,limit)
    return {"customers": customers}

@app.post("/customers")
def create_customer(user_input: CustomerCreate):
    """
    Create a new customer in the 'users' table.
    Returns the newly created user object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_customer_db(con, user_input)
    except ValueError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    return {
        "id": inserted["id"],
        "username": user_input.username
    }
@app.post("/realtors")
def create_realtor(user_input: RealtorCreate):
    """
    Create a new realtor in the 'users' table.
    Returns the newly created user object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_realtor_db(con, user_input)
    except ValueError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    return {
        "id": inserted["id"],
        "username": user_input.username
    }
@app.post("/realtor_reviews")
def create_realtor_review(user_input: RealtorReviewCreate):
    """
    Create a new realtor review in the 'users' table.
    Returns the newly created realtor review object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_realtor_review_db(con, user_input)
    except ValueError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    return {
        "id": inserted["id"]
    }
@app.post("/real_estates")
def create_real_estates(user_input: RealestateCreate):
    """
    Create a new realtor in the 'users' table.
    Returns the newly created user object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_real_estate_db(con, user_input)
    except ValueError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    return {
        "id": inserted["id"]
  
    }

@app.post("/ads")
def create_ad(user_input: AdCreate):
    """
    Create a new ad in the 'ads' table.
    Returns the newly created ad object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_ad_db(con, user_input)
    except ValueError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    return {
        "id": inserted["id"]
    #    "ad": ad_input.ad
    }


@app.delete("/customers/{customer_id}")
def delete_user(customer_id: int):
    """Delete a user by ID."""
    con = get_connection()
    try:
        delete_customer_db(con,customer_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="customer not found")
    return {"message": f"User with ID {customer_id} deleted successfully."}

@app.delete("/realtors/{realtor_id}")
def delete_realtor(realtor_id: int):
    """Delete a realtor by ID."""
    con = get_connection()
    try:
        delete_realtor_db(con,realtor_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="real estate not found")
    return {"message": f"Realtor with ID {realtor_id} deleted successfully."}

@app.delete("/realtor_reviews/{realtor_review_id}")
def delete_realtor_review(realtor_review_id: int):
    """Delete a realtor by ID."""
    con = get_connection()
    try:
        delete_realtor_review_db(con,realtor_review_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="real review not found")
    return {"message": f"Realtor review with ID {realtor_review_id} deleted successfully."}

@app.delete("/real_estates/{real_estate_id}")
def delete_real_estate(real_estate_id: int):
    """Delete a real estate by ID."""
    con = get_connection()
    try:
        delete_real_estate_db(con,real_estate_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="real estate not found")
    return {"message": f"Real restate with ID {real_estate_id} deleted successfully."}

@app.delete("/ads/{ad_id}")
def delete_ad(ad_id: int):
    """Delete a ad by ID."""
    con = get_connection()
    try:
        delete_ad_db(con,ad_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ad not found")
    return {"message": f"Ad with ID {ad_id} deleted successfully."}

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer_update: CustomerUpdate):
    """
    updates customer's data. all fields must be included and updated.
    Returns the updated customer object.
    """
    con = get_connection()
    try:
        result=update_customer_db(con,customer_id, customer_update)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return result

@app.put("/realtors/{realtor_id}")
def update_realtor(realtor_id: int, realtor_update: RealtorUpdate):
    """
    updates realtor's data. all fields must be included and updated.
    Returns the updated customer object.
    """
    con = get_connection()
    try:
        result=update_realtor_db(con,realtor_id, realtor_update)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return result

@app.put("/realtor_reviews/{realtor_review_id}")
def update_realtor_review(realtor_review_id: int, realtor_review_update: RealtorReviewUpdate):
    """
    updates realtor's data. all fields must be included and updated.
    Returns the updated customer object.
    """
    con = get_connection()
    try:
        result=update_realtor_review_db(con,realtor_review_id, realtor_review_update)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return result

@app.put("/real_estates/{real_estate_id}")
def update_real_estate(real_estate_id: int, real_estate_update: RealestateUpdate):
    """
    updates real estate's data. all fields must be included and updated.
    Returns the updated customer object.
    """
    con = get_connection()
    try:
        result=update_real_estate_db(con,real_estate_id, real_estate_update)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return result

@app.put("/ads/{ad_id}")
def update_ad(ad_id: int, ad_update: AdUpdate):
    """
    updates ad's data. all fields must be included and updated.
    Returns the updated ad object.
    """
    con = get_connection()
    try:
        result=update_ad_db(con,ad_id, ad_update)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="Foreign Key error")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return result

@app.patch("/customers/{customer_id}")
def patch_customer(customer_id: int, customer_patch: CustomerPatch):
    """
    Partially updates customer's data. Not all fields must be included and updated in the request.
    Returns the updated customer object.
    """
    update_data = customer_patch.model_dump(exclude_unset=True)  # only provided fields
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    con = get_connection()
    try:
        result=patch_customer_db(con,customer_id, update_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="customer not found")
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result

 