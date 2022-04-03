# coinbase pro class that accesses the coinbase pro api
import coinbasepro  as cbp
import pandas as pd
import itertools
import datetime as dt

class Coin:

    def __init__(self) -> None:
        client = cbp.PublicClient()
        self.client = client

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
