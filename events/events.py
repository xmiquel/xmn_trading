class DataEvent:
    def __init__(self, symbol, timeframe, timestamp, bid, ask):
        self.symbol = symbol
        self.timeframe = timeframe
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask

class SignalEvent:
    def __init__(self, strategy_name, signal_type, data_event):
        self.strategy_name = strategy_name
        self.signal_type = signal_type
        self.data_event = data_event

class SizingEvent:
    def __init__(self, strategy_name, signal_event):
        self.strategy_name = strategy_name
        self.signal_event = signal_event
        self.position_size = 0

class OrderEvent:
    def __init__(self, strategy_name, signal_event, sizing_event):
        self.strategy_name = strategy_name
        self.signal_event = signal_event
        self.sizing_event = sizing_event

class ExecutionEvent:
    def __init__(self, strategy_name, order_event, execution_result):
        self.strategy_name = strategy_name
        self.order_event = order_event
        self.execution_result = execution_result

class CloseEvent:
    def __init__(self, position_id):
        self.position_id = position_id

class NotificationEvent:
    def __init__(self, message):
        self.message = message
