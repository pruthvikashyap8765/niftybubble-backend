from fastapi import FastAPI, APIRouter
import yfinance as yf
import numpy as np
import redis
import json
import time
import os




# Redis Cloud Credentials
REDIS_HOST = "redis-11740.c301.ap-south-1-1.ec2.redns.redis-cloud.com"
REDIS_PORT = 11740  
REDIS_PASSWORD = "2aAjcmt84lVmNDGTN1wmo8bU3yYs9UfZ"
# Connect to Redis Cloud
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,  # Redis Cloud requires authentication
    decode_responses=True
)

# Test the connection
try:
    redis_client.ping()
    print("Successfully connected to Redis Cloud!")
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")







router = APIRouter(
    prefix='/stocks',
    tags=['Stock Data']
)

NIFTY_50_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS",
    "ICICIBANK.NS", "INFY.NS", "BAJFINANCE.NS", "SBIN.NS",
    "HINDUNILVR.NS", "ITC.NS", "LT.NS", "HCLTECH.NS",
    "SUNPHARMA.NS", "MARUTI.NS", "KOTAKBANK.NS", "M&M.NS",
    "AXISBANK.NS", "BAJAJFINSV.NS", "NTPC.NS", "WIPRO.NS",
    "ULTRACEMCO.NS", "ONGC.NS", "TITAN.NS", "ADANIENT.NS",
    "TATAMOTORS.NS", "POWERGRID.NS", "JSWSTEEL.NS", "ADANIPORTS.NS",
    "BAJAJ-AUTO.NS", "COALINDIA.NS", "NESTLEIND.NS", "ASIANPAINT.NS",
    "BEL.NS", "TRENT.NS", "TATASTEEL.NS", "TECHM.NS",
    "GRASIM.NS", "SBILIFE.NS", "HINDALCO.NS", "EICHERMOT.NS",
    "HDFCLIFE.NS", "CIPLA.NS", "BRITANNIA.NS", "SHRIRAMFIN.NS",
    "BPCL.NS", "TATACONSUM.NS", "DRREDDY.NS", "APOLLOHOSP.NS",
    "INDUSINDBK.NS", "HEROMOTOCO.NS"
]

@router.get("/")
def stockdata():
    cache_key = "stock_data"

    # Check if data exists in Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Serving data from cache")
        return json.loads(cached_data)  # Return cached data

    print("Fetching fresh data from Yahoo Finance")
    data = []
    for ticker in NIFTY_50_TICKERS:
        try:
            company_data = yf.Ticker(ticker)
            hourly_data = company_data.history(period="1d", interval="1h")

            if hourly_data.empty:
                continue

            volume_24h = int(np.sum(hourly_data['Volume']))
            hourly_data = hourly_data.iloc[:, :4]

            daily_data = company_data.history(period="1y")
            if daily_data.empty:
                continue

            hourly_change = round(
                float((hourly_data['Close'][-1] - hourly_data['Close'][-2]) / hourly_data['Close'][-2] * 100),
                2) if len(hourly_data) > 1 else 0
            daily_change = round(
                float((daily_data['Close'][-1] - daily_data['Close'][-2]) / daily_data['Close'][-2] * 100), 2) if len(
                daily_data) > 1 else 0
            weekly_change = round(
                float((daily_data['Close'][-1] - daily_data['Close'][-5]) / daily_data['Close'][-5] * 100), 2) if len(
                daily_data) > 5 else 0
            monthly_change = round(
                float((daily_data['Close'][-1] - daily_data['Close'][-30]) / daily_data['Close'][-30] * 100), 2) if len(
                daily_data) > 30 else 0
            yearly_change = round(
                float((daily_data['Close'][-1] - daily_data['Close'][0]) / daily_data['Close'][0] * 100), 2) if len(
                daily_data) > 0 else 0

            info = company_data.info
            current_price = info.get('currentPrice')
            market_cap = info.get('marketCap')

            new_data = {
                "name": ticker[:-3],
                "price": current_price,
                "hourly_change": hourly_change,
                "daily_change": daily_change,
                "weekly_change": weekly_change,
                "monthly_change": monthly_change,
                "yearly_change": yearly_change,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
            }

            data.append(new_data)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # Store in Redis cache for 60 minutes
    redis_client.setex(cache_key, 3600, json.dumps(data))

    return data
