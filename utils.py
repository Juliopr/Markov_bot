# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np



def get_kline_df(client,symbol="BTCUSDT",KL_INTERVAL='1h',days=10):
    """
    

    Parameters
    ----------
    client : binance.client.Client
        A isntacia do cliente para binance.
        
    symbol : str, optional
        O simobolo do ativo que ira requisitar os kadles. O default é "BTCUSDT".
        
        
    KL_INTERVAL : str, optional
        Os parametros de tempo da binance mais comins [5m,15m,1h,2h,4h]. O default é '1h'.
        
        
    days : int, optional
        O número de dias em que ira puxar o intervalo de kandles. O default é 10.

    Returns
    -------
    df : pd.DataFrame
        Um dataframe com os dados de data,abertura,alta, minima,fechamento,volume.

    """    

    
    #Baixamos os dados de kandle da binance
    klines = client.get_historical_klines(symbol,
                                        KL_INTERVAL,
                                     "{} day ago UTC".format(days))
    
    
    #converto para um dataframe
    df = pd.DataFrame(klines, columns = ['ts', 'o', 'h', 'l',
                                         'c','v',
                                         'close_time', 'quote_av',
                                         'trades', 'tb_base_av',
                                         'tb_quote_av', 'ignore' ])
    
    #Fazemos o pré-processamento básico
    df=df.apply(pd.to_numeric)
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df=df.set_index('ts')
    
    return df




def make_interval(data,intervals_number=10):
    """
    

    Parameters
    ----------
    data : pd.Series
        A série temporal para a qual iremos gerar intervalo.
        
        
    intervals_number : int, optional
        A quantidade de intervalos no qual iremos dividir a série temporal.
        O default é 10.

    Returns
    -------
    intervals : list
        Lista contendo os intervalos
    
    intervals_label: um dict que associa uma label a cada média do intervalo

    """
    
    inter = (data.max() - data.min())/intervals_number
    
    in_iter = data.min()
    #final_interval = data.max()
    
    intervals = []
    i = 0
    for x in range(intervals_number):
        
        if i == 0:
            intervals.append([in_iter,in_iter + ((i+1)*inter)])
        
        # elif i == intervals_number:
        #     intervals.append([final_interval])
            
        else:
            intervals.append([in_iter + (i*inter), 
                              in_iter + ((i+1)*inter)])
        
        i += 1
        
        
    intervals_label = {}
    i = 0
    
    for interval in intervals:
        
        intervals_label[i] = (interval[0] + interval[1])/2
        i += 1
    
    return intervals,intervals_label



def compute_states(data,inters):
    """
    

    Parameters
    ----------
    data : pd.Series
        A série temporal na qual iremos converter para intervalos.
        
    intervals : list
        A lista de tuplas contendo os intervalos calculados a partir da séries.

    Returns
    -------
    states : list
        Os valores convertido para valores discreto. Onde o número represent
        o index do intervalo que ele pertence.

    """
    
    states = []
    for price in data.values:
        
        
        #print(price)
        i = 0
        for itv in inters:

            #Faço o teste para o primeiro intervalo
            if i == 0 and price <= itv[0]:
                 states.append(i)
            
            if i == (len(inters) - 1) and price >= itv[1]:
                 states.append(i)


            else:
                
                if (price >= itv[0]) and  (price <= itv[1]):
                    states.append(i)
                    break



            i += 1

    return states



def transition_matrix(states,intervals):
    """
    

    Parameters
    ----------
    states : list
        A lista contendo todos os estados
        no intervalo de tempo    
    
    intervals : list
        Lista de tuplas contendo todos os
        intervalos os intervalos de preços
        para aquele periodo.
        

    Returns
    -------
    numpy.array
        A matriz de probabilidade de
        transição de um estado N para
        o esta M. 
        Utilizada para medir a
        probabilidade de transição
        para o próximo estado.
        
    """

    
    n = len(intervals) #number of states

    M = [[0]*n for _ in range(n)]

    for (i,j) in zip(states,states[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return np.array(M)
