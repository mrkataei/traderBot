import pandas as pd

from Analysis.diamond import Diamond

from Analysis.ruby import Ruby
name='ETHUSDT4h'
#%% create dataset with label



file = pd.read_csv('Static/'+name+'.csv')

print(len(file))
result=[]
for i in range(len(file)-1):
    print(i)
    compare = (file.iloc[i])['close'] - (file.iloc[i + 1])['close']
    if compare < 0 :
        result.append('buy')
    elif compare > 0:
        result.append('sell')
    else:
        result.append('none')
file=file[:-1]
file['result']=result

file.to_csv('Static/'+name+'-withLable'+'.csv')
#%%


name_label='ETHUSDT4h-withLable'

file = pd.read_csv('Static/'+name_label+'.csv')
file.head()

#%% diamond_output


settings = {'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                                 'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
            'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                                   'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                                   'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}}


diamond=Diamond(data=file, coin_id=2, timeframe_id=3, gain=1, bot_ins=1, setting=settings, cost=1)

diamond_output=diamond.get_recommendations()

diamond_output.to_csv('Static/'+name+'-diamond-output'+'.csv')



#%% ruby_output
settings = {'analysis_setting': {'delay':13 ,'safe_line':-8603 ,'hist_line':0 },
            'indicators_setting': {'MACD': {'slow': 17, 'signal': 9, 'fast': 4, 'source': 'close', 'matype': 'sma'}}}


ruby=Ruby(data=file,gain=1,cost=1,coin_id=2,timeframe_id=3,bot_ins=1,setting=settings)
ruby_output=ruby.get_recommendations()
ruby_output.to_csv('Static/'+name+'-ruby-output'+'.csv')

#%% concat_all_data


