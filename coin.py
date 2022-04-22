# coinbase pro class that accesses the coinbase pro api
# from this import d
import coinbasepro  as cbp
import pandas as pd
import numpy as np
import itertools
import datetime as dt
import plotly.graph_objects as go

class Coin:

    def __init__(self) -> None:
        client = cbp.PublicClient()
        self.client = client
    
    def trade_charts(self, trading_pair):
        client = self.client
        data = pd.DataFrame(client.get_product_historic_rates(trading_pair))
        data = data.iloc[::-1]
        fig = go.Figure(
                # title=trading_pair,
                data=[go.Candlestick(x=data['time'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])
        fig.update_layout(title=trading_pair)
        # fig.show()
        # fig.to_image(format="png", engine="kaleido")
        fig.write_image("charts/{}.png".format(trading_pair))
        
        # return data

    # calculates a crossover strategyfor the current crypto pair
    def trade_signal(self, ticker):
        client = self.client
        data = pd.DataFrame(client.get_product_historic_rates(ticker))
        data = data.iloc[::-1]
        data['slow_MA'] = data['close'].rolling(16).mean() # moving average = trend path
        data['fast_MA'] = data['close'].rolling(6).mean() 
        data['buy'] = np.where(data['fast_MA']  > data['slow_MA'], 1, 0)
        data['sell'] = np.where(data['fast_MA'] < data['slow_MA'], 1, 0)
        data['position'] = np.where(data['buy'] == 1, 'buy', 'sell')
        data.dropna(inplace=True)
        position = data.iloc[-1]['position']
        return position, ticker

    def setup_pair_data(self):
        client = self.client
        data = pd.DataFrame(client.get_products())
        data['id'].to_csv('data/pair_labels.csv')
        data.to_csv('data/pairs.csv')

    def all_available_pairs(self):        
        products = pd.read_csv('data/pair_labels.csv')
        return products
    
    def recent_trades(self, ticker, trade_count):
        client = self.client

        try:
            trades = list(itertools.islice(client.get_product_trades(ticker), trade_count))

            trade_data = pd.DataFrame(columns= ['time', 'trade_id', 'size', 'price', 'side'])

            for i in range(trade_count):
                
                trade_data = trade_data.append({
                    'time' : trades[i]['time'],
                    'trade_id' : trades[i]['trade_id'],
                    'size' : trades[i]['size'],
                    'price' : trades[i]['price'],
                    'side' : trades[i]['side']
                    
                }, ignore_index=True)
        
        except Exception as e:
            print(e)
            
        return trades
