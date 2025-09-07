from questdb_stock import insert_latest_quote, get_latest_price

# Insert a new quote
success = insert_latest_quote("AAPL", "NASDAQ", 189.23)
print("Insert successful:", success)

# Fetch latest price
latest_price = get_latest_price("AAPL", "NASDAQ")
print("Latest price:", latest_price)

################################################

from questdb_interface import (
    insert_stock_price,
    insert_customer_position,
    get_positions_by_customer,
    get_positions_by_customer_and_stock
)

# Insert stock price
insert_stock_price("AAPL", "NASDAQ", 189.23)

# Insert customer position
insert_customer_position("CUST001", "AAPL", "NASDAQ", "BUY", 100, 189.23, "Initial buy")

# Query all positions for a customer
positions = get_positions_by_customer("CUST001")
print("All positions:", positions)

# Query positions for a customer and stock
apple_positions = get_positions_by_customer_and_stock("CUST001", "AAPL")
print("AAPL positions:", apple_positions)

from questdb_interface import get_latest_stock_price

latest_price = get_latest_stock_price("AAPL", "NASDAQ")
print("Latest AAPL price:", latest_price)