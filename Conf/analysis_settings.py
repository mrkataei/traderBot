diamond_btcusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_ethusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_adausdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_etcusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_bchusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_dogeusdt_30m = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
ruby_dogeusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}

diamond_conf = {
    'coins':
        {
            1: {'timeframes': {3: diamond_btcusdt_4h}},
            2: {'timeframes': {3: diamond_ethusdt_4h}},
            3: {'timeframes': {3: diamond_ethusdt_4h}},
            4: {'timeframes': {1: diamond_ethusdt_4h}},
            5: {'timeframes': {3: diamond_ethusdt_4h}},
            6: {'timeframes': {3: diamond_ethusdt_4h}}
        }
}

ruby_conf = {
    'coins':
        {
            2: {'timeframes': {3}, 'settings': ruby_dogeusdt_4h}
        }
}
analysis_con = {
    'analysis':
        {
            3: diamond_conf,
            2: ruby_conf
        }
}


def get_analysis_setting(coin_id: int, timeframe_id: int, analysis_id: int):
    if coin_id in analysis_con['analysis'][analysis_id]['coins'] \
            and timeframe_id in analysis_con['analysis'][analysis_id]['coins'][coin_id]['timeframes']:
        return analysis_con['analysis'][analysis_id]['coins'][coin_id]['timeframes'][timeframe_id]
    else:
        return False

