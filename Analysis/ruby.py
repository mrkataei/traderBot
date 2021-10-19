import pandas as pd
import numpy as np
from Libraries.tools import Tools, cross_over, get_source
from Libraries.macd import macd

valid_coins_and_times = {
    'coins':
        {
            2: {'timeframes': {3}}
        }
}


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, bot_ins, settings: dict,
           symbol: str, timeframe: str):
    if coin_id in valid_coins_and_times['coins'] \
            and timeframe_id in valid_coins_and_times['coins'][coin_id]['timeframes']:
        ruby_tools = Tools(analysis_id=2, timeframe_id=timeframe_id, coin_id=coin_id)
        delay = settings['analysis_setting']['delay']
        safe_line = settings['analysis_setting']['safe_line']
        hist_line = settings['analysis_setting']['hist_line']
        slow = settings['indicators_setting']['MACD']['slow']
        sign = settings['indicators_setting']['MACD']['signal']
        fast = settings['indicators_setting']['MACD']['fast']
        matype = settings['indicators_setting']['MACD']['matype']
        source = settings['indicators_setting']['MACD']['source']
        source = get_source(data=data, source=source)
        print("ruby checking ... " + symbol, timeframe)

        # create macd dataframe macd has 3 column original macd , histogram  and signal
        macd_df = macd(close=source, slow=slow, fast=fast, signal=sign, matype=matype)
        macd_df.columns = ["macd", "histogram", "signal"]
        # add price of coin to the macd_df
        macd_df["close"] = data.close

        safe_line = safe_line / 100.0

        last_macd = np.array(macd_df.tail(2))
        close = float(last_macd[1, 3])

        last_data = ruby_tools.get_last_data(start_position=False)
        old_position = last_data[0]
        old_price = last_data[1]

        if cross_over(last_macd[:, 1], hist_line) and \
                last_macd[1, 0] < - safe_line and old_position == "sell":
            print("buy")
            result = True, "medium"
            ruby_tools.signal_process(close=close, gain=gain, result=result, cost=cost, bot_ins=bot_ins)

        elif float(last_macd[1, 1]) < np.array(macd_df.tail(delay)["histogram"])[0] and \
                old_price < close and old_position == "buy":
            print("sell")
            result = False, "medium"
            ruby_tools.signal_process(close=close, gain=gain, result=result, cost=cost, bot_ins=bot_ins)
