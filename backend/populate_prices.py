import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import alpaca_trade_api as tradeapi

load_dotenv()

# Connect to PlanetScale DB
connection = mysql.connector.connect(
host=os.getenv("HOST"),
database=os.getenv("DATABASE"),
user=os.getenv("DB_USER"),
password=os.getenv("PASSWORD"),
ssl_ca=os.getenv("SSL_CERT")
)
try:
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
except Error as e:
    print("Error while connecting to MySQL", e)

# Connect to Alpaca Markets API
HEADERS = {'APCA-API-KEY-ID': os.getenv("ALPACA_KEY"),
           'APCA-API-SECRET-KEY': os.getenv("ALPACA_SECRET")}

api = tradeapi.REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), os.getenv("ALPACA_BASE_URL"))

# DEFINE GLOBAL VARS
symbols = []
stock_dict = {}

# DB FUNCTIONS - get all symbols
sql = "SELECT * from stock"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']
    
def insertPrices(symbol, date, high, open, low, close, volume):
    stock_id = stock_dict[symbol]
    insert_stmt = "INSERT IGNORE INTO stock_price (stock_id, date, high, open, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (stock_id, date, high, open, low, close, volume)
    cursor.execute(insert_stmt, data)
    # connection.commit()
    
#######
    
# ITERATE BARS OF MANY STOCK DATA
def get_stocks_bars(symbols):
    bar_iter = api.get_bars_iter(symbols, tradeapi.TimeFrame.Day, "2022-07-01", "2023-01-01", adjustment='raw')
    prevSymbol = ''    
    for bar in (bar_iter):
        # print(bar)
        # print(bar.S, symbol)
        if bar.S in symbols:
            if bar.S != prevSymbol:
                prevSymbol = bar.S
                print(f"Processing bars for {bar.S}")
            insertPrices(bar.S, bar.t, bar.h, bar.o, bar.l, bar.c, bar.v)
    connection.commit()




# GET 200 SIZE CHUNKS OF STOCKS TO FETCH PRICES OF
chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    # print(i)
    # print(i+chunk_size)
    symbol_chunk = symbols[i:i+chunk_size]
    # print(symbol_chunk)
    get_stocks_bars(symbol_chunk)