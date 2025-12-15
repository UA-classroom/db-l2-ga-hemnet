import os

import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from db import get_all_customers_db, get_customer_db, add_customer_db, delete_customer_db, patch_customer_db, update_customer_db
from db import get_all_ads_db, get_ad_db, add_ad_db#, delete_ad_db, update_ad_db
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from schemas import (
    CustomerCreate, CustomerUpdate,CustomerPatch,
    AdCreate, AdUpdate
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
        raise HTTPException(status_code=404, detail="customer not found")

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
#"""
##@app.post("/customers")
##def create_customer(customer_input: CustomerCreate):
##    """
##    Create a new customer in the 'users' table.
##    Returns the newly created customer object with its ID.
##    """
##    con = get_connection()
##    try:
##        inserted = add_customer_db(con, customer_input)
##    except ValueError:
##        raise HTTPException(status_code=409, detail="username or email already exists")
##    except psycopg2.errors.ForeignKeyViolation:
##        raise HTTPException(status_code=409, detail="Foreign Key error")
##    except psycopg2.errors.UniqueViolation:
##        raise HTTPException(status_code=409, detail="Unique constraint violated")
##    return {
##        "id": inserted["id"],
##        "username": customer_input.username
##    }
#"""
@app.post("/ads")
def create_ad(ad_input: AdCreate):
    """
    Create a new ad in the 'ads' table.
    Returns the newly created ad object with its ID.
    """
    con = get_connection()
    try:
        inserted = add_ad_db(con, ad_input)
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

#@app.put("/customer/{customer_id}", response_model=CustomerUpdate)
@app.put("/customer/{customer_id}")
def update_customer(customer_id: int, customer_update: CustomerUpdate):
    """
    Partially updates customer's data. all fields must be included and updated.
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
#    except psycopg2.errors.ForeignKeyViolation:
#        raise HTTPException(status_code=409, detail="Foreign Key error")
#    except psycopg2.errors.UniqueViolation:
#        raise HTTPException(status_code=409, detail="Unique constraint violated")
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result

 