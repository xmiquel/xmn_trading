import asyncio
import logging
import MetaTrader5 as mt5
from engine.event_manager import EventManager
from events.events import DataEvent
from strategies.bollinger_rsi_strategy import BollingerRSIStrategy

class MetaTrader5Broker:
    def __init__(self):
        mt5.initialize()
        self.logger = logging.getLogger('trading_framework.MetaTrader5Broker')

    def send_order(self, symbol, action, volume):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid if action == 'buy' else mt5.symbol_info_tick(symbol).ask,
            "deviation": 20,
            "magic": 234000,
            "comment": "Python trading",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        self.logger.info(f'Orden enviada: {request}')
        return result

    def close_position(self, position_id):
        result = mt5.position_close(position_id)
        self.logger.info(f'Posición cerrada: {position_id}')
        return result

    def get_execution_details(self, order):
        pass


if __name__ == '__main__':
    event_manager = EventManager()
    broker = MetaTrader5Broker()
    strategy = BollingerRSIStrategy()

    event_manager.register_strategy(strategy)
    event_manager.set_broker(broker)

    # Simulación de recepción de eventos de datos y encolado
    data_event = DataEvent('CL', '2024-08-07 12:00:00', 74.25, 74.30)
    event_manager.add_event(data_event)

    # Iniciar el procesamiento de eventos
    asyncio.run(event_manager.start())
