# -*- coding: utf-8 -*-
from binance.client import Client
import config
import utils


#Instanciamos o cliente da binance.
client = Client(config.API_KEY,
                        config.API_SECRET)


KL_DAYS = 10
KL_INTERVAL = '1h'
SYMBOL = "BTCUSDT"



#Baixamos os dados da binance e colocamos em um dataframe
df = utils.get_kline_df(client,symbol=SYMBOL,
                        KL_INTERVAL=KL_INTERVAL,days=KL_DAYS)

intervals,labels = utils.make_interval(df['c'],intervals_number=15)

states = utils.compute_states(df['c'],intervals)

TM = utils.transition_matrix(states,intervals)

