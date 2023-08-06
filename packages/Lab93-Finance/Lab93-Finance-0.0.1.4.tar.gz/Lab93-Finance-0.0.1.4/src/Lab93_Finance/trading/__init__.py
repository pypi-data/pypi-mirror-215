from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import TimeInForce, OrderSide

class TradeBroker:
    def __init__( self, client ):
         self.MarketOrder = MarketOrderRequest
         self.LimitOrder = LimitOrderRequest

         self.SELL = OrderSide.SELL
         self.BUY = OrderSide.BUY
         
         self.GTC = TimeInForce.GTC