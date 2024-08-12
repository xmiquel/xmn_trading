import asyncio
import logging
from queue import Queue

from events.events import CloseEvent, DataEvent, ExecutionEvent, NotificationEvent, OrderEvent, SignalEvent, SizingEvent

class EventManager:
    def __init__(self):
        self.event_queue = Queue()
        self.strategies = []
        self.broker = None
        self.logger = logging.getLogger('trading_framework.EventManager')

    def register_strategy(self, strategy):
        self.strategies.append(strategy)
        self.logger.info(f'Estrategia {strategy.name} registrada.')

    def set_broker(self, broker):
        self.broker = broker
        self.logger.info('Broker configurado.')

    def add_event(self, event):
        self.event_queue.put(event)
        self.logger.debug(f'Evento añadido a la cola: {event}')

    async def process_events(self):
        while True:
            if not self.event_queue.empty():
                event = self.event_queue.get()
                self.logger.debug(f'Procesando evento: {event}')
                await self.process_event(event)
            else:
                await asyncio.sleep(0.1)  # Espera corta si no hay eventos

    async def process_event(self, event):
        if isinstance(event, DataEvent):
            for strategy in self.strategies:
                signal_event = strategy.add_data(event.symbol, event.timestamp, event.bid, event.ask)
                if signal_event:
                    self.add_event(signal_event)
        elif isinstance(event, SignalEvent):
            for strategy in self.strategies:
                if strategy.name == event.strategy_name:
                    sizing_event = strategy.handle_sizing_event(event)
                    self.add_event(sizing_event)
        elif isinstance(event, SizingEvent):
            for strategy in self.strategies:
                if strategy.name == event.strategy_name:
                    order_event = strategy.handle_order_event(event)
                    self.add_event(order_event)
        elif isinstance(event, OrderEvent):
            execution_result = self.broker.send_order(
                event.sizing_event.signal_event.data_event.symbol,
                event.sizing_event.signal_event.signal_type,
                event.sizing_event.position_size
            )
            execution_event = ExecutionEvent(
                event.strategy_name, event, execution_result
            )
            self.add_event(execution_event)
        elif isinstance(event, CloseEvent):
            self.broker.close_position(event.position_id)
        elif isinstance(event, NotificationEvent):
            self.logger.info(f'Notificación: {event.message}')

        self.logger.debug(f'Evento procesado correctamente: {event}')


    async def start(self):
        await self.process_events()
