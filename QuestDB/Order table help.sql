












from questdb_interface import (
    insert_customer_order,
    get_orders_by_customer,
    get_order_by_id
)

# Insert a new order
insert_customer_order(
    order_id="ORD123456",
    customer_id="CUST001",
    stock_name="AAPL",
    exchange_name="NASDAQ",
    order_type="BUY",
    execution_type="LIMIT",
    position_type="INTRADAY",
    order_status="PENDING",
    price=189.50,
    quantity=100,
    notes="Limit order placed during market open"
)

# Query all orders for a customer
orders = get_orders_by_customer("CUST001")
print("Customer orders:", orders)

# Query a specific order
order = get_order_by_id("ORD123456")
print("Order details:", order)




CREATE TABLE customer_orders (
    timestamp TIMESTAMP,             -- Time of order placement
    order_id SYMBOL,                 -- Unique order identifier
    customer_id SYMBOL,              -- Customer placing the order
    stock_name SYMBOL,               -- Stock involved
    exchange_name SYMBOL,            -- Exchange (e.g., NSE, NASDAQ)
    order_type SYMBOL,               -- 'BUY' or 'SELL'
    execution_type SYMBOL,           -- 'MARKET' or 'LIMIT'
    position_type SYMBOL,            -- 'INTRADAY' or 'POSITIONAL'
    order_status SYMBOL,             -- 'PENDING', 'COMPLETED', 'REJECTED'
    price DOUBLE,                    -- Order price
    quantity LONG,                   -- Number of shares
    notes STRING                     -- Optional remarks
) timestamp(timestamp);

#Get all orders for a customer:
SELECT * FROM customer_orders
WHERE customer_id = 'CUST001'
ORDER BY timestamp DESC;

#Get a specific order by ID

SELECT * FROM customer_orders
WHERE order_id = 'ORD123456';

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from questdb_interface import (
    insert_algo_subscription,
    cancel_algo_subscription,
    get_algo_subscriptions_by_customer,
    get_active_algo_subscriptions
)

# Add a new subscription
insert_algo_subscription("CUST001", "MomentumAlgo", "2025-09-06", notes="Subscribed via dashboard")

# Cancel a subscription
cancel_algo_subscription("CUST001", "MomentumAlgo", "2025-09-06")

# Get all subscriptions
all_subs = get_algo_subscriptions_by_customer("CUST001")
print("All subscriptions:", all_subs)

# Get active subscriptions
active_subs = get_active_algo_subscriptions("CUST001")
print("Active subscriptions:", active_subs)