from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
# from simulation.ma_cross import run_ma_sim
from dateutil import parser
from infrastructure.collect_data import run_collection
from simulation.ema_macd import run_ema_macd


if __name__ == '__main__':
    # api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    # run_collection(instrumentCollection, api)
    # run_ma_sim()
    run_ema_macd(instrumentCollection)
