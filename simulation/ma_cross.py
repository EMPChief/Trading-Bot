import pandas as pd
from infrastructure.instrument_collection import Instrument, InstrumentCollection as ic

ic = ic()
BUY = 1
SELL = 2
NONE = 0
get_ma_col = lambda x: f"MA__{x}"

def is_trade(row, ma_l, ma_s):
    """
    Determine the trade signal based on the relationship between moving averages.

    Parameters:
    - row (pd.Series): The row of the DataFrame.
    - ma_l (str): Column name for the long-term moving average.
    - ma_s (str): Column name for the short-term moving average.

    Returns:
    - int: Trade signal (BUY, SELL, or NONE).

    The function compares the changes in moving averages to generate trade signals:
    - If the current delta (difference between ma_s and ma_l) is non-negative, and the previous delta was negative, it returns BUY.
    - If the current delta is negative, and the previous delta was non-negative, it returns SELL.
    - Otherwise, it returns NONE.
    """
    if row.DELTA >= 0 and row.DELTA_PREV < 0:
        return BUY
    if row.DELTA < 0 and row.DELTA_PREV >= 0:
        return SELL
    return NONE
def load_price_data(pair, granularity, ma_list):
    """
    Load price data for a given currency pair and granularity.

    Parameters:
    - pair (str): Currency pair (e.g., "EUR_USD").
    - granularity (str): Time granularity of the data (e.g., "H1").
    - ma_list (list): List of moving averages to calculate.

    Returns:
    - pd.DataFrame: Loaded price data.
    """
    df = pd.read_pickle(f"./data/{pair}_{granularity}.pkl")
    for ma in ma_list:
        df[get_ma_col(ma)] = df.mid_c.rolling(window=ma).mean()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_trades(df_analysis, instrument):
    """
    Extract trades and calculate total gain.

    Parameters:
    - df_analysis (pd.DataFrame): DataFrame with analysis data.
    - instrument (Instrument): Financial instrument information.

    Returns:
    - dict: Dictionary containing total gain and DataFrame with trades.
    """
    df_trades = df_analysis[df_analysis.TRADE != NONE].copy()
    df_trades['DIFF'] = df_trades.mid_c.diff().shift(-1)
    df_trades.fillna(0, inplace=True)
    df_trades['GAIN'] = df_trades['DIFF'] / instrument.pipLocation
    df_trades['GAIN'] = df_trades['GAIN'] * df_trades['TRADE']
    total_gain = df_trades['GAIN'].sum()
    return dict(total_gain=total_gain, df_trades=df_trades)

def assess_pair(price_data, ma_l, ma_s, instrument):
    """
    Assess trading performance for a specific currency pair and moving averages.

    Parameters:
    - price_data (pd.DataFrame): DataFrame containing price data.
    - ma_l (str): Column name for the long-term moving average.
    - ma_s (str): Column name for the short-term moving average.
    - instrument (Instrument): Financial instrument information.

    Returns:
    - dict: Dictionary containing total gain and DataFrame with trades.
    """
    df_analysis = price_data.copy()
    df_analysis['DELTA'] = df_analysis[ma_s] - df_analysis[ma_l]
    df_analysis['DELTA_PREV'] = df_analysis['DELTA'].shift(1)
    df_analysis['TRADE'] = df_analysis.apply(lambda row: is_trade(row, ma_l, ma_s), axis=1)
    return get_trades(df_analysis, instrument)

def analyse_pair(instrument, granularity, ma_long, ma_short):
    """
    Analyze trading performance for different combinations of moving averages.

    Parameters:
    - instrument (Instrument): Financial instrument information.
    - granularity (str): Time granularity of the data (e.g., "H1").
    - ma_long (list): List of long-term moving averages.
    - ma_short (list): List of short-term moving averages.
    """
    ma_list = set(ma_long + ma_short)
    pair = instrument.name
    
    price_data = load_price_data(pair, granularity, ma_list)
    
    for ma_l in ma_long:
        for ma_s in ma_short:
            if ma_l == ma_s:
                continue
            result = assess_pair(
                price_data,
                get_ma_col(ma_l),
                get_ma_col(ma_s),
                instrument
            )
            tg = result['total_gain']
            nt = result['df_trades'].shape[0]
            print(f"Pair name: {pair}\nGranularity: {granularity}\nMA Long: {ma_l}\nMA Short: {ma_s}\nTotal Gain: {tg}\nHow many trades: {nt}")

def run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "CHF", "AUD"],
               granularity=["H1"],
               ma_long=[20, 40, 80],
               ma_short=[10, 20]):
    """
    Run a moving average simulation for multiple currency pairs and moving averages.

    Parameters:
    - curr_list (list): List of currency pairs.
    - granularity (list): List of time granularities.
    - ma_long (list): List of long-term moving averages.
    - ma_short (list): List of short-term moving averages.
    """
    ic.LoadInstruments("./data")
    for g in granularity:
        for p1 in curr_list:
            for p2 in curr_list:
                pair = f"{p1}_{p2}"
                if pair in ic.instruments_dict.keys():
                    analyse_pair(ic.instruments_dict[pair], g, ma_long, ma_short)

