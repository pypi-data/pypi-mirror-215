from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests   import CryptoLatestQuoteRequest

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests   import StockLatestQuoteRequest


class PriceData:
    def __init__(self, asset_type, credentials):


        self.asset_type = asset_type.lower()

        if self.asset_type   == "stocks":
            self.client = StockHistoricalDataClient( credentials[0],
                                                     credentials[1] )

        elif self.asset_type == "crypto":
            self.client = CryptoHistoricalDataClient( credentials[0],
                                                      credentials[1] )


    def CurrentPrice(self, symbol):


        if self.asset_type == "stocks":
            parameters = StockLatestQuoteRequest( symbol_or_symbols = symbol )
            quote = self.client\
                        .get_stock_latest_quote( parameters )

        elif self.asset_type == "crypto":
            parameters = CryptoLatestQuoteRequest( symbol_or_symbols = symbol )
            quote = self.client\
                        .get_crypto_latest_quote( parameters )

        return quote[symbol].ask_price