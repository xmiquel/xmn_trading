import asyncio
from engine.event_manager import EventManager
from broker.metatrader5_broker import MetaTrader5Broker
from strategies.bollinger_rsi_strategy import BollingerRSIStrategy
from data.market_data import get_and_store_candle_data
import config

if __name__ == '__main__':
    # Inicializar la conexión a la base de datos
    conn = config.get_db_connection()

    # Inicializar el gestor de eventos
    event_manager = EventManager(conn)
    broker = MetaTrader5Broker()

    symbols = ['EURUSD', 'GBPUSD']  # Ejemplo de símbolos
    timeframes = ['1H', '4H']  # Ejemplo de temporalidades

    for symbol in symbols:
        for timeframe in timeframes:
            strategy = BollingerRSIStrategy(symbol, timeframe, conn)
            event_manager.register_strategy(strategy)
    
    event_manager.set_broker(broker)

    # Obtener y almacenar datos de mercado
    for symbol in symbols:
        for timeframe in timeframes:
            get_and_store_candle_data(symbol, timeframe, conn)

    # Iniciar el procesamiento de eventos
    asyncio.run(event_manager.start())
