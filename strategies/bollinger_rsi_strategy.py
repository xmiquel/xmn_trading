import logging
import pandas as pd
import pandas_ta as ta
from psycopg2 import sql
from events.events import SignalEvent, SizingEvent, OrderEvent

class BollingerRSIStrategy:
    def __init__(self):
        self.name = 'BollingerRSIStrategy'
        self.data = pd.DataFrame()
        self.logger = logging.getLogger('trading_framework.BollingerRSIStrategy')

    def add_data(self, symbol, timestamp, bid, ask):
        new_data = {'timestamp': timestamp, 'bid': bid, 'ask': ask, 'close': (bid + ask) / 2}
        self.data = self.data.append(new_data, ignore_index=True)

        if len(self.data) > 20:
            self.data.ta.rsi(length=14, append=True)
            self.data.ta.bbands(length=20, std=2, append=True)

            latest_data = self.data.iloc[-1]
            return self.generate_signal(latest_data)

    def generate_signal(self, latest_data):
        if latest_data['RSI_14'] < 30 and latest_data['close'] < latest_data['BBL_20_2.0']:
            signal_event = SignalEvent(self.name, 'buy', latest_data)
            self.logger.info('Generada señal de compra.')
            return signal_event
        elif latest_data['RSI_14'] > 70 and latest_data['close'] > latest_data['BBU_20_2.0']:
            signal_event = SignalEvent(self.name, 'sell', latest_data)
            self.logger.info('Generada señal de venta.')
            return signal_event
        return None

    def handle_sizing_event(self, signal_event):
        sizing_event = SizingEvent(self.name, signal_event)
        sizing_event.position_size = 1  # Ejemplo simple: tamaño de posición fijo
        self.logger.info('Determinado tamaño de posición.')
        return sizing_event

    def handle_order_event(self, sizing_event):
        order_event = OrderEvent(self.name, sizing_event.signal_event, sizing_event)
        self.logger.info('Generada orden de trading.')
        return order_event
