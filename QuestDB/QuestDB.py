# questdb_stock.py

from questdb.ingress import Sender, TimestampNanos, Protocol
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configuration
QUESTDB_HOST = "localhost"
INGRESS_PORT = 9000
PG_PORT = 8812
USERNAME = "admin"
PASSWORD = "quest"
TABLE_NAME = "stock_prices"

# Insert latest quote
def insert_latest_quote(stock_name: str, exchange_name: str, price: float) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_NAME,
                symbols={"stock_name": stock_name, "exchange_name": exchange_name},
                columns={"price": price},
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Insertion failed: {e}")
        return False

# Get latest price for a stock
def get_latest_price(stock_name: str, exchange_name: str) -> float | None:
    try:
        conn = psycopg2.connect(
            host=QUESTDB_HOST,
            port=PG_PORT,
            user=USERNAME,
            password=PASSWORD,
            dbname="qdb"
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = f"""
                SELECT stock_name, exchange_name, price, timestamp
                FROM {TABLE_NAME}
                WHERE stock_name = %s AND exchange_name = %s
                ORDER BY timestamp DESC
                LIMIT 1;
            """
            cur.execute(query, (stock_name, exchange_name))
            result = cur.fetchone()
            return result["price"] if result else None
    except Exception as e:
        print(f"Query failed: {e}")
        return None


from questdb_interface import get_latest_stock_price

latest_price = get_latest_stock_price("AAPL", "NASDAQ")
print("Latest AAPL price:", latest_price)

# Insert a new job
insert_jobber_job(
    jobber_id="JOB001",
    customer_id="CUST001",
    security="AAPL",
    start_price=90000,
    step_size_buy=500,
    direction="LONG",
    step_size_sell=750,
    lot_multiplier="FLAT",
    no_of_steps=10,
    re_enter=True,
    end_date="2025-12-31",
    auto_rollover=True,
    active=True,
    deleted=False,
    notes="Initial setup"
)

# Retrieve job
job = get_jobber_job("JOB001")
print("Job details:", job)

# Mark job as deleted
delete_jobber_job("JOB001", notes="Removed by user")

# Toggle active status
toggle_jobber_job_active("JOB001", active=False, notes="Paused by user")



CREATE TABLE customer_profiles (
    timestamp TIMESTAMP,             -- Time of record creation
    customer_id SYMBOL,              -- Unique customer identifier
    customer_name STRING,            -- Full name
    phone STRING,                    -- Phone number
    email STRING,                    -- Email address
    consent BOOLEAN,                 -- Consent flag
    user_id SYMBOL,                  -- Login user ID
    password_hash STRING,            -- Hashed password
    registration_date DATE,          -- Date of registration
    active BOOLEAN,                  -- Active/inactive status
    deleted BOOLEAN,                 -- Logical deletion flag
    notes STRING                     -- Optional metadata
) timestamp(timestamp);


# Create a new customer
insert_customer_profile(
    customer_id="CUST001",
    customer_name="John Doe",
    phone="9876543210",
    email="john@example.com",
    consent=True,
    user_id="john_doe",
    password_hash="hashed_password_here",
    registration_date="2025-09-07",
    active=True
)

# Retrieve by email
profile = get_customer_profile_by("email", "john@example.com")
print("Customer profile:", profile)

# Mark customer as deleted
delete_customer_profile("CUST001")

# Update active status
update_customer_active_status("CUST001", active=False, notes="User deactivated account")

