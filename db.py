import psycopg2
from fastapi import FastAPI, HTTPException
from psycopg2 import errors, sql
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""
customer_type=1
realtor_type=2

def build_partial_update_query(update_data: dict, table: str, pk: str = "id"):
    # Convert {"field": value} into "field = %s" clauses
    set_clauses = []
    params = []

    for column_name, value in update_data.items():
        # Safely quote column names with Identifier
        set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(column_name)))
        params.append(value)  # value may be None (→ NULL)

    if not set_clauses:
        return None, None

    # Build UPDATE with RETURNING
    query = sql.SQL("""
        UPDATE {table}
        SET {set_clause}
        WHERE {pk} = %s
        RETURNING *
    """).format(
        table=sql.Identifier(table),
        set_clause=sql.SQL(", ").join(set_clauses),
        pk=sql.Identifier(pk),
    )

    params.append(None)  # last param is PK (filled by caller)
    return query, params

def get_all_customers_db(con,limit):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE type = %s LIMIT %s;", (customer_type,limit))
            items = cursor.fetchall()
    return items
def get_customer_db(con, customer_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("SELECT * FROM users where id=%s;",
                           (customer_id))
                items = cursor.fetchall()
            except Exception:
                raise ValueError("Customer ID not valid")
    return items
def get_all_ads_db(con,limit):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM ads LIMIT %s;", (limit,))
            items = cursor.fetchall()
    return items
def get_ad_db(con, customer_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("SELECT * FROM users where id=%s;",
                           (customer_id))
                items = cursor.fetchall()
            except Exception:
                raise ValueError("Customer ID not valid")
    return items
def get_all_realtor_reviews_db(con,limit):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM realtor_reviews LIMIT %s;", (limit,))
            items = cursor.fetchall()
    return items

def add_customer_db(con,user_input):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                type=customer_type

                cursor.execute(
                    "INSERT INTO users (type, user_name, user_psw, email) VALUES (%s,%s,%s,%s) RETURNING id;",
                    (type, user_input.username, user_input.password, user_input.email)
                )
                inserted = cursor.fetchone()
                id = inserted["id"]
                cursor.execute(
                    "INSERT INTO customer_profiles (id,adress) VALUES (%s,%s) RETURNING id;",
                    (id,user_input.adress)
                )
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except Exception:
                raise ValueError("DB error")
    return inserted

def add_realtor_db(con,user_input):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                type=realtor_type
                cursor.execute(
                    "INSERT INTO users (type, user_name, user_psw, email) VALUES (%s,%s,%s,%s) RETURNING id;",
                    (type, user_input.username, user_input.password, user_input.email)
                )
                inserted = cursor.fetchone()
                id = inserted["id"]
                cursor.execute(
                    "INSERT INTO realtor_profiles (id,agency) VALUES (%s,%s) RETURNING id;",
                    (id,user_input.agency)
                )
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except Exception:
                raise ValueError("DB error")
    return inserted

def add_real_estate_db(con,user_input):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "INSERT INTO real_estates (real_estate_type, municipal, adress, living_space, no_of_rooms) VALUES (%s,%s,%s,%s,%s) RETURNING id;",
                    (user_input.real_estate_type, user_input.municipal, user_input.adress, user_input.living_space, user_input.no_of_rooms)
                )
                inserted = cursor.fetchone()
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except Exception:
                raise ValueError("DB error")
    return inserted

def add_realtor_review_db(con,user_input):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "INSERT INTO realtor_reviews (originator, realtor, score, comment) VALUES (%s,%s,%s,%s) RETURNING id;",
                    (user_input.originator, user_input.realtor, user_input.score, user_input.comment)
                )
                inserted = cursor.fetchone()
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except Exception:
                raise ValueError("DB error")
    return inserted

def add_ad_db(con,ad_input):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "INSERT INTO ads (agreement, customer, publish_date, end_date, realtor, description, price, sold_price, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
                    (ad_input.agreement, ad_input.customer, ad_input.publish_date, ad_input.end_date, ad_input.realtor,ad_input.description,ad_input.price,ad_input.sold_price,ad_input.status)
                )
                inserted = cursor.fetchone()
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except Exception:
                raise ValueError("DB error")
    return inserted


def delete_customer_db(con, customer_id: int):
    """Delete a user by ID."""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (customer_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("User not found")           
            except ValueError:
                raise ValueError("User not found")
    return

def delete_realtor_db(con, realtor_id: int):
    """Delete a realtor by ID."""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (realtor_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("User not found")           
            except ValueError:
                raise ValueError("User not found")
    return
def delete_realtor_review_db(con, realtor_review_id: int):
    """Delete a realtor by ID."""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("DELETE FROM realtor_reviews WHERE id = %s RETURNING id;", (realtor_review_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("realtor review not found")           
            except ValueError:
                raise ValueError("realtor review not found")
    return

def delete_real_estate_db(con, real_estate_id: int):
    """Delete a real estate by ID."""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("DELETE FROM real_estates WHERE id = %s RETURNING id;", (real_estate_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("Real estate not found")           
            except ValueError:
                raise ValueError("Real estate not found")
    return

def delete_ad_db(con, ad_id: int):
    """Delete a user by ID."""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute("DELETE FROM ads WHERE id = %s RETURNING id;", (ad_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("Ad not found")           
            except ValueError:
                raise ValueError("Ad not found")
    return

def update_customer_db(con, customer_id: int, customer_update):
    """
    updates a customer's data.
    Returns the updated customer object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "UPDATE users SET type=%s, user_name=%s, user_psw=%s, email=%s, name=%s WHERE id=%s RETURNING *;",
                    (customer_type, customer_update.username, customer_update.password, customer_update.email, customer_update.name, customer_id)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Customer not found")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except ValueError:
                raise ValueError("customer does not exist")
    return row
def update_realtor_db(con, realtor_id: int, realtor_update):
    """
    updates a realtor's data.
    Returns the updated realtor object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "UPDATE users SET type=%s, user_name=%s, user_psw=%s, email=%s, name=%s WHERE id=%s RETURNING *;",
                    (realtor_type, realtor_update.username, realtor_update.password, realtor_update.email, realtor_update.name, realtor_id)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Customer not found")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except ValueError:
                raise ValueError("customer does not exist")
    return row
def update_realtor_review_db(con, realtor_review_id: int, realtor_review_update):
    """
    updates a realtor's data.
    Returns the updated realtor object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "UPDATE realtor_reviews SET originator=%s, realtor=%s, score=%s, comment=%s WHERE id=%s RETURNING *;",
                    (realtor_review_update.originator, realtor_review_update.realtor, realtor_review_update.score, realtor_review_update.comment, realtor_review_id)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Customer not found")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except ValueError:
                raise ValueError("customer does not exist")
    return row

def update_real_estate_db(con, real_estate_id: int, real_estate_update):
    """
    updates a real estate's data.
    Returns the updated real estate object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "UPDATE real_estates SET real_estate_type=%s, municipal=%s, adress=%s, living_space=%s, no_of_rooms=%s WHERE id=%s RETURNING *;",
                    (real_estate_update.real_estate_type, real_estate_update.municipal, real_estate_update.adress, real_estate_update.living_space, real_estate_update.no_of_rooms, real_estate_id)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Real estate not found")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except ValueError:
                raise ValueError("real estate does not exist")
    return row

def update_ad_db(con, ad_id: int, ad_update):
    """
     updates an ad's data.
    Returns the updated ad object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    "UPDATE ads SET agreement=%s, customer=%s, publish_date=%s, end_date=%s, realtor=%s, description=%s, price=%s, sold_price=%s, status=%s WHERE id=%s RETURNING *;",
                    (ad_update.agreement, ad_update.customer, ad_update.publish_date, ad_update.end_date, ad_update.realtor, ad_update.description, ad_update.price, ad_update.sold_price, ad_update.status, ad_id)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError("ad not found")
            except psycopg2.errors.ForeignKeyViolation:
                raise psycopg2.errors.ForeignKeyViolation ("Foreign Key error")
            except psycopg2.errors.UniqueViolation:
                raise psycopg2.errors.UniqueViolation("Unique error")
            except ValueError:
                raise ValueError("ad does not exist")
    return row

def patch_customer_db(con,customer_id, update_data):
    print(update_data)
    query, params = build_partial_update_query(update_data, table="users", pk="id")
    params[-1] = customer_id  # set PK
    print(query)

    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, tuple(params))
                row = cur.fetchone()

                if not row:
                    raise HTTPException(status_code=404, detail="User not found")

                # return safe fields only
                return {
                    "id": row["id"],
                    "username": row.get("username"),
                    "email": row.get("email"),
                    "created_at": row.get("created_at"),
                }

    except errors.UniqueViolation:
        raise errors.UniqueViolation("Unique constraint violated")
    except Exception as e:
        raise Exception(e)



