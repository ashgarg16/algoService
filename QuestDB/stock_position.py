# questdb_interface.py

from questdb.ingress import Sender, TimestampNanos, Protocol
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
QUESTDB_HOST = "localhost"
INGRESS_PORT = 9000
PG_PORT = 8812
USERNAME = "admin"
PASSWORD = "quest"

# Table names
TABLE_STOCK_PRICES = "stock_prices"
TABLE_CUSTOMER_POSITIONS = "customer_positions"
TABLE_CUSTOMER_ORDERS = "customer_orders"
TABLE_CUSTOMER_ALGO_SUBSCRIPTIONS = "customer_algo_subscriptions"
TABLE_JOBBER_JOBS = "jobber_jobs"
TABLE_CUSTOMER_PROFILES = "customer_profiles"

# Insert into stock_prices
def insert_stock_price(stock_name: str, exchange_name: str, price: float) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_STOCK_PRICES,
                symbols={"stock_name": stock_name, "exchange_name": exchange_name},
                columns={"price": price},
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Stock price insertion failed: {e}")
        return False

# Get latest price for a stock
def get_latest_stock_price(stock_name: str, exchange_name: str) -> float | None:
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
                SELECT price
                FROM {TABLE_STOCK_PRICES}
                WHERE stock_name = %s AND exchange_name = %s
                ORDER BY timestamp DESC
                LIMIT 1;
            """
            cur.execute(query, (stock_name, exchange_name))
            result = cur.fetchone()
            return result["price"] if result else None
    except Exception as e:
        print(f"Latest price query failed: {e}")
        return None

# Insert into customer_positions
def insert_customer_position(
    customer_id: str,
    stock_name: str,
    exchange_name: str,
    position_type: str,
    quantity: int,
    price: float,
    notes: str = ""
) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_CUSTOMER_POSITIONS,
                symbols={
                    "customer_id": customer_id,
                    "stock_name": stock_name,
                    "exchange_name": exchange_name,
                    "position_type": position_type
                },
                columns={
                    "quantity": quantity,
                    "price": price,
                    "notes": notes
                },
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Customer position insertion failed: {e}")
        return False

# Query all positions by customer ID
def get_positions_by_customer(customer_id: str) -> list:
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
                SELECT * FROM {TABLE_CUSTOMER_POSITIONS}
                WHERE customer_id = %s
                ORDER BY timestamp DESC;
            """
            cur.execute(query, (customer_id,))
            return cur.fetchall()
    except Exception as e:
        print(f"Query failed: {e}")
        return []

# Query positions by customer ID and stock name
def get_positions_by_customer_and_stock(customer_id: str, stock_name: str) -> list:
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
                SELECT * FROM {TABLE_CUSTOMER_POSITIONS}
                WHERE customer_id = %s AND stock_name = %s
                ORDER BY timestamp DESC;
            """
            cur.execute(query, (customer_id, stock_name))
            return cur.fetchall()
    except Exception as e:
        print(f"Query failed: {e}")
        return []
    
def insert_customer_order(
    order_id: str,
    customer_id: str,
    stock_name: str,
    exchange_name: str,
    order_type: str,
    execution_type: str,
    position_type: str,
    order_status: str,
    price: float,
    quantity: int,
    notes: str = ""
) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_CUSTOMER_ORDERS,
                symbols={
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "stock_name": stock_name,
                    "exchange_name": exchange_name,
                    "order_type": order_type,
                    "execution_type": execution_type,
                    "position_type": position_type,
                    "order_status": order_status
                },
                columns={
                    "price": price,
                    "quantity": quantity,
                    "notes": notes
                },
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Order insertion failed: {e}")
        return False

# Query all orders by customer ID
def get_orders_by_customer(customer_id: str) -> list:
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
                SELECT * FROM {TABLE_CUSTOMER_ORDERS}
                WHERE customer_id = %s
                ORDER BY timestamp DESC;
            """
            cur.execute(query, (customer_id,))
            return cur.fetchall()
    except Exception as e:
        print(f"Order query failed: {e}")
        return []

# Query a specific order by order ID
def get_order_by_id(order_id: str) -> dict | None:
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
                SELECT * FROM {TABLE_CUSTOMER_ORDERS}
                WHERE order_id = %s;
            """
            cur.execute(query, (order_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Order lookup failed: {e}")
        return None


# Insert a new subscription
def insert_algo_subscription(
    customer_id: str,
    algo_name: str,
    subscription_date: str,  # Format: 'YYYY-MM-DD'
    status: str = "ACTIVE",
    notes: str = ""
) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_CUSTOMER_ALGO_SUBSCRIPTIONS,
                symbols={
                    "customer_id": customer_id,
                    "algo_name": algo_name,
                    "status": status
                },
                columns={
                    "subscription_date": subscription_date,
                    "notes": notes
                },
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Subscription insertion failed: {e}")
        return False

# Cancel a subscription (logical delete)
def cancel_algo_subscription(
    customer_id: str,
    algo_name: str,
    subscription_date: str,
    notes: str = "Cancelled by user"
) -> bool:
    return insert_algo_subscription(
        customer_id=customer_id,
        algo_name=algo_name,
        subscription_date=subscription_date,
        status="CANCELLED",
        notes=notes
    )

# Query all subscriptions for a customer
def get_algo_subscriptions_by_customer(customer_id: str) -> list:
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
                SELECT * FROM {TABLE_CUSTOMER_ALGO_SUBSCRIPTIONS}
                WHERE customer_id = %s
                ORDER BY subscription_date DESC;
            """
            cur.execute(query, (customer_id,))
            return cur.fetchall()
    except Exception as e:
        print(f"Subscription query failed: {e}")
        return []

# Query active subscriptions for a customer
def get_active_algo_subscriptions(customer_id: str) -> list:
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
                SELECT * FROM {TABLE_CUSTOMER_ALGO_SUBSCRIPTIONS}
                WHERE customer_id = %s AND status = 'ACTIVE'
                ORDER BY subscription_date DESC;
            """
            cur.execute(query, (customer_id,))
            return cur.fetchall()
    except Exception as e:
        print(f"Active subscription query failed: {e}")
        return []




# Insert a new job
def insert_jobber_job(
    jobber_id: str,
    customer_id: str,
    security: str,
    start_price: float,
    step_size_buy: float,
    direction: str,
    step_size_sell: float,
    lot_multiplier: str,
    no_of_steps: int,
    re_enter: bool,
    end_date: str,  # Format: 'YYYY-MM-DD'
    auto_rollover: bool,
    active: bool,
    deleted: bool = False,
    notes: str = ""
) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_JOBBER_JOBS,
                symbols={
                    "jobber_id": jobber_id,
                    "customer_id": customer_id,
                    "security": security,
                    "direction": direction,
                    "lot_multiplier": lot_multiplier
                },
                columns={
                    "start_price": start_price,
                    "step_size_buy": step_size_buy,
                    "step_size_sell": step_size_sell,
                    "no_of_steps": no_of_steps,
                    "re_enter": re_enter,
                    "end_date": end_date,
                    "auto_rollover": auto_rollover,
                    "active": active,
                    "deleted": deleted,
                    "notes": notes
                },
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Job insertion failed: {e}")
        return False

# Retrieve job by Jobber_ID
def get_jobber_job(jobber_id: str) -> dict | None:
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
                SELECT * FROM {TABLE_JOBBER_JOBS}
                WHERE jobber_id = %s AND deleted = false
                ORDER BY timestamp DESC
                LIMIT 1;
            """
            cur.execute(query, (jobber_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Job retrieval failed: {e}")
        return None

# Mark job as deleted
def delete_jobber_job(jobber_id: str, notes: str = "Marked as deleted") -> bool:
    try:
        job = get_jobber_job(jobber_id)
        if not job:
            print("Job not found.")
            return False
        return insert_jobber_job(
            jobber_id=job["jobber_id"],
            customer_id=job["customer_id"],
            security=job["security"],
            start_price=job["start_price"],
            step_size_buy=job["step_size_buy"],
            direction=job["direction"],
            step_size_sell=job["step_size_sell"],
            lot_multiplier=job["lot_multiplier"],
            no_of_steps=job["no_of_steps"],
            re_enter=job["re_enter"],
            end_date=job["end_date"],
            auto_rollover=job["auto_rollover"],
            active=job["active"],
            deleted=True,
            notes=notes
        )
    except Exception as e:
        print(f"Failed to mark job as deleted: {e}")
        return False

# Toggle job active status
def toggle_jobber_job_active(jobber_id: str, active: bool, notes: str = "") -> bool:
    try:
        job = get_jobber_job(jobber_id)
        if not job:
            print("Job not found.")
            return False
        return insert_jobber_job(
            jobber_id=job["jobber_id"],
            customer_id=job["customer_id"],
            security=job["security"],
            start_price=job["start_price"],
            step_size_buy=job["step_size_buy"],
            direction=job["direction"],
            step_size_sell=job["step_size_sell"],
            lot_multiplier=job["lot_multiplier"],
            no_of_steps=job["no_of_steps"],
            re_enter=job["re_enter"],
            end_date=job["end_date"],
            auto_rollover=job["auto_rollover"],
            active=active,
            deleted=job["deleted"],
            notes=notes
        )
    except Exception as e:
        print(f"Toggle failed: {e}")
        return False
    
# Table name


# Create a new customer record
def insert_customer_profile(
    customer_id: str,
    customer_name: str,
    phone: str,
    email: str,
    consent: bool,
    user_id: str,
    password_hash: str,
    registration_date: str,  # Format: 'YYYY-MM-DD'
    active: bool,
    deleted: bool = False,
    notes: str = ""
) -> bool:
    try:
        with Sender(Protocol.HTTP, QUESTDB_HOST, INGRESS_PORT, username=USERNAME, password=PASSWORD) as sender:
            sender.row(
                table=TABLE_CUSTOMER_PROFILES,
                symbols={
                    "customer_id": customer_id,
                    "user_id": user_id
                },
                columns={
                    "customer_name": customer_name,
                    "phone": phone,
                    "email": email,
                    "consent": consent,
                    "password_hash": password_hash,
                    "registration_date": registration_date,
                    "active": active,
                    "deleted": deleted,
                    "notes": notes
                },
                at=TimestampNanos.now()
            )
            sender.flush()
        return True
    except Exception as e:
        print(f"Customer profile insertion failed: {e}")
        return False

# Retrieve customer by any identifier
def get_customer_profile_by(field: str, value: str) -> dict | None:
    try:
        if field not in ["customer_id", "email", "phone", "user_id"]:
            raise ValueError("Invalid field for lookup")
        conn = psycopg2.connect(
            host=QUESTDB_HOST,
            port=PG_PORT,
            user=USERNAME,
            password=PASSWORD,
            dbname="qdb"
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = f"""
                SELECT * FROM {TABLE_CUSTOMER_PROFILES}
                WHERE {field} = %s AND deleted = false
                ORDER BY timestamp DESC
                LIMIT 1;
            """
            cur.execute(query, (value,))
            return cur.fetchone()
    except Exception as e:
        print(f"Customer lookup failed: {e}")
        return None

# Mark customer as deleted
def delete_customer_profile(customer_id: str, notes: str = "Marked as deleted") -> bool:
    try:
        profile = get_customer_profile_by("customer_id", customer_id)
        if not profile:
            print("Customer not found.")
            return False
        return insert_customer_profile(
            customer_id=profile["customer_id"],
            customer_name=profile["customer_name"],
            phone=profile["phone"],
            email=profile["email"],
            consent=profile["consent"],
            user_id=profile["user_id"],
            password_hash=profile["password_hash"],
            registration_date=profile["registration_date"],
            active=profile["active"],
            deleted=True,
            notes=notes
        )
    except Exception as e:
        print(f"Failed to delete customer: {e}")
        return False

# Update active status
def update_customer_active_status(customer_id: str, active: bool, notes: str = "") -> bool:
    try:
        profile = get_customer_profile_by("customer_id", customer_id)
        if not profile:
            print("Customer not found.")
            return False
        return insert_customer_profile(
            customer_id=profile["customer_id"],
            customer_name=profile["customer_name"],
            phone=profile["phone"],
            email=profile["email"],
            consent=profile["consent"],
            user_id=profile["user_id"],
            password_hash=profile["password_hash"],
            registration_date=profile["registration_date"],
            active=active,
            deleted=profile["deleted"],
            notes=notes
        )
    except Exception as e:
        print(f"Failed to update active status: {e}")
        return False


