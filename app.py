# -*- coding: utf-8 -*-
from binance.client import Client
import config
import utils
import telegram
import time


#Instanciamos o cliente da binance.
client = Client(config.API_KEY,
                        config.API_SECRET)

#Instanciamos o bot do telegram
bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)

KL_DAYS = 15
KL_INTERVAL = '1h'
SYMBOL = "BTCUSDT"


#Vamos iniciar um loop
while True:
    
    #Baixamos os dados da binance e colocamos em um dataframe
    df = utils.get_kline_df(client,symbol=SYMBOL,
                        KL_INTERVAL=KL_INTERVAL,days=KL_DAYS)
    
    #IMPORTANTE: o ultimo Kandle que binance libera
    #ainda não foi fechado.
    #Então eu pego ate apenas o penultimo
    #pois o ultimo não foi concluido ainda
    df = df.iloc[:-1]
    
    
    #Fazemos o intervalo
    intervals,labels = utils.make_interval(df['c'],
                                           intervals_number=15)
    
    #Calculamos os estados
    states = utils.compute_states(df['c'],intervals)
    
    #Calculamos a matriz de transição
    TM = utils.transition_matrix(states,intervals)
    
    #aqui irei pegar o ultimo estado
    #lembre que esse vai nos da o 
    #index da matriz com a probabilidade dos próximos estados
    next_state_proba = TM[states[-1]]
    
    #Agora irei fazer um dict do tipo estado =>probabilidade
    next_states_indexes = next_state_proba.argsort()[-3:][::-1]    
    next_probas = next_state_proba[next_states_indexes]
    
    proba_dict = dict(zip(next_states_indexes,next_probas))
    
    #Veja que o chat_id representa o id que coletamos momentos atras.
    bot.send_message(text='markov status:{}'.format(states[-1]), chat_id=-760818082)
    bot.send_message(text=str(proba_dict),
                      chat_id=-760818082)
                                    
    #Coloco para dormi por 10 minutos
    time.sleep(600)
    
    
    
    