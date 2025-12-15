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

def update_customer_db(con, customer_id: int, customer_update):
    """
    Partially updates a movie's data.
    Returns the updated movie object.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            #type=1
            try:
                cursor.execute(
                    "UPDATE users SET type=%s, user_name=%s, user_psw=%s, email=%s, name=%s WHERE id=%s RETURNING *;",
                    (customer_update.type, customer_update.username, customer_update.password, customer_update.email, customer_update.name, customer_id)
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



