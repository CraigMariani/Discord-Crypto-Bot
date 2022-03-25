# coinbase pro class that accesses the coinbase pro api
import coinbasepro  as cbp
import pandas as pd

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


