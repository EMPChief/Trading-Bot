from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from streaming.streamer import run_streaming_application
from db.db import DataBaseMongo
from scraping.class_tradingeconomics_com import TradingEconomicsCalendar

def db_test():
    db = DataBaseMongo()
    d = db.query_distinct(DataBaseMongo.LEARNING_COLLECTION, "hate")
    print(d)


if __name__ == '__main__':
#    api = OandaApi()
#    instrumentCollection.LoadInstruments("./data")
#    run_streaming_application()
    calendar = TradingEconomicsCalendar()
    calendar.fetch_and_save_to_database()

