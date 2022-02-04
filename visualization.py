# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from binance.client import Client
import config
import utils
import plotly.graph_objects as go
import plotly.io as pio


pio.renderers.default='browser'




#Instanciamos o cliente da binance.
client = Client(config.API_KEY,
                        config.API_SECRET)


KL_DAYS = 10
KL_INTERVAL = '1h'
SYMBOL = "BTCUSDT"





#Baixamos os dados da binance e colocamos em um dataframe
df = utils.get_kline_df(client,symbol=SYMBOL,KL_INTERVAL=KL_INTERVAL,days=KL_DAYS)

intervals,labels = utils.make_interval(df['c'],intervals_number=15)

states = utils.compute_states(df['c'],intervals)

discretes = [labels[x] for x in states]


fig=go.Figure()


fig.add_trace(go.Candlestick(x=df.index,
                                      open=df['o'],
                                      high=df['h'],
                                      low=df['l'],
                                      close=df['c']))

fig.add_trace(go.Line(x=df.index,
                      y=discretes,
                      line_color="#0000ff"))


fig.update_layout(xaxis_title = 'X', yaxis_title = 'Y')

fig.show()