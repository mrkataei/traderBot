diamond_btcusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 25, 'stoch_k_overbuy': 75, 'stoch_rsi_k_oversell': 20,
                         'stoch_rsi_k_overbuy': 69, 'rsi_oversell': 37, 'rsi_overbuy': 63},
    'indicators_setting': {'RSI': {'length': 7, 'source': 'close'}, 'stoch': {'k': 17, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 15, 'length': 24, 'source': 'close'},
                           'MACD': {'slow': 21, 'signal': 20, 'fast': 5, 'source': 'close', 'matype': 'ema'}}
}

diamond_ethusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 28, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
                         'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 73},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
                           'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}
}
diamond_adausdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 37, 'stoch_k_overbuy': 91, 'stoch_rsi_k_oversell': 14,
                         'stoch_rsi_k_overbuy': 92, 'rsi_oversell': 45, 'rsi_overbuy': 64},
    'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 4, 'd': 2, 'rsi_length': 14, 'length': 21, 'source': 'ohlc4'},
                           'MACD': {'slow': 18, 'signal': 20, 'fast': 12, 'source': 'hlc3', 'matype': 'ema'}}
}
diamond_etcusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 10, 'stoch_k_overbuy': 91, 'stoch_rsi_k_oversell': 84,
                         'stoch_rsi_k_overbuy': 55, 'rsi_oversell': 81, 'rsi_overbuy': 88},
    'indicators_setting': {'RSI': {'length': 5, 'source': 'close'}, 'stoch': {'k': 18, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 23, 'length': 16, 'source': 'high'},
                           'MACD': {'slow': 36, 'signal': 20, 'fast': 11, 'source': 'close', 'matype': 'ema'}}
}
diamond_bchusdt_4h = {
    'analysis_setting': {'stoch_k_oversell': 17, 'stoch_k_overbuy': 93, 'stoch_rsi_k_oversell': 8,
                         'stoch_rsi_k_overbuy': 69, 'rsi_oversell': 36, 'rsi_overbuy': 85},
    'indicators_setting': {'RSI': {'length': 7, 'source': 'close'}, 'stoch': {'k': 20, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 4, 'd': 3, 'rsi_length': 21, 'length': 6, 'source': 'hlc3'},
                           'MACD': {'slow': 15, 'signal': 20, 'fast': 9, 'source': 'close', 'matype': 'ema'}}
}
diamond_dogeusdt_30m = {
    'analysis_setting': {'stoch_k_oversell': 20, 'stoch_k_overbuy': 92, 'stoch_rsi_k_oversell': 18,
                         'stoch_rsi_k_overbuy': 96, 'rsi_oversell': 29, 'rsi_overbuy': 62},
    'indicators_setting': {'RSI': {'length': 5, 'source': 'close'}, 'stoch': {'k': 23, 'd': 3, 'smooth': 3},
                           'stochrsi': {'k': 5, 'd': 3, 'rsi_length': 20, 'length': 12, 'source': 'ohlc4'},
                           'MACD': {'slow': 18, 'signal': 20, 'fast': 13, 'source': 'ohlc4', 'matype': 'ema'}}
}


diamond_conf = {
    'coins':
        {
            1: {'timeframes': {3: diamond_btcusdt_4h}},
            2: {'timeframes': {3: diamond_ethusdt_4h}},
            3: {'timeframes': {3: diamond_adausdt_4h}},
            6: {'timeframes': {1: diamond_dogeusdt_30m}},
            5: {'timeframes': {3: diamond_bchusdt_4h}},
            4: {'timeframes': {3: diamond_etcusdt_4h}}
        }
}

analysis_con = {
    'analysis':
        {
            3: diamond_conf
        }
}


def get_analysis_setting(coin_id: int, timeframe_id: int, analysis_id: int):
    if coin_id in analysis_con['analysis'][analysis_id]['coins'] \
            and timeframe_id in analysis_con['analysis'][analysis_id]['coins'][coin_id]['timeframes']:
        return analysis_con['analysis'][analysis_id]['coins'][coin_id]['timeframes'][timeframe_id]
    else:
        return False
