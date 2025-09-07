from fastapi import FastAPI
from app.routers import (
    stock_price,
    customer_profile,
    customer_order,
    customer_position,
    jobber_job,
    algo_subscription,
    client_broker
)

app = FastAPI(title="Trading System API")

app.include_router(stock_price.router)
app.include_router(customer_profile.router)
app.include_router(customer_order.router)
app.include_router(customer_position.router)
app.include_router(jobber_job.router)
app.include_router(algo_subscription.router)
app.include_router(client_broker.router)

