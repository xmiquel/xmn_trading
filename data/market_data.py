import MetaTrader5 as mt5
from datetime import datetime
import psycopg2

def save_candle_data(symbol, timeframe, timestamp, close, db_connection):
    query = """
    INSERT INTO market_data (symbol, timeframe, timestamp, close) 
    VALUES (%s, %s, %s, %s) 
    ON CONFLICT DO NOTHING
    """
    with db_connection.cursor() as cursor:
        cursor.execute(query, (symbol, timeframe, timestamp, close))
        db_connection.commit()

def get_and_store_candle_data(symbol, timeframe, db_connection):
    mt5_timeframe = {
        '1H': mt5.TIMEFRAME_H1,
        '4H': mt5.TIMEFRAME_H4
    }[timeframe]
    
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, 1000)
    for rate in rates:
        save_candle_data(symbol, timeframe, datetime.fromtimestamp(rate['time']), rate['close'], db_connection)
