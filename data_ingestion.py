import firebase_admin
from firebase_admin import credentials, db
import yfinance as yf
import os
import json
from datetime import datetime

# Load Firebase credentials from environment variable
firebase_key = json.loads(os.environ.get("FIREBASE_KEY"))
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("DATABASE_URL")
})

def fetch_and_store_stock_data(ticker="AAPL", period="1d"):
    # Fetch data
    stock = yf.Ticker(ticker)
    data = stock.history(period=period).reset_index()
    
    # Convert datetime to string for Firebase
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Push to Firebase
    ref = db.reference(f'/market_data/{ticker}')
    for _, row in data.iterrows():
        ref.push().set(row.to_dict())
    print(f"Data for {ticker} ingested successfully!")

if __name__ == "__main__":
    fetch_and_store_stock_data("AAPL", "1d")  # Daily data for Apple
