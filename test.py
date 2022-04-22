from coin import Coin
import pandas as pd

# Coin.recent_trades('BTC-USD')
c = Coin()

ticker = 'BTC-USD'
# ticker = 'ETH-USD'
data = c.trade_charts(ticker)
print(data)
# count = 2
# trades = c.recent_trades('BTC-USD', count)


# trade_data = pd.DataFrame(columns= ['time', 'trade_id', 'size', 'price', 'side'])

# for i in range(count):
    
#     trade_data = trade_data.append({
#         'time' : trades[i]['time'],
#         'trade_id' : trades[i]['trade_id'],
#         'size' : trades[i]['size'],
#         'price' : trades[i]['price'],
#         'side' : trades[i]['side']
        
#     }, ignore_index=True)

# print(trade_data)
# data ={
#     'time':[],
#     'trade_id':[],
#     'size':[],
#     'price':[],
#     'side':[]
# }
# pd.DataFrame(data)