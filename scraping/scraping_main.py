from scrape_class.dailyfx_com import DailyFXScraper
from scrape_class.investing_com import InvestingComScraper
from scrape_class.reuters_com import ReutersComScraper
from scrape_def.scraper_defs import scrape_dailyfx_data, scrape_investor_data, scrape_reuters_data
import time

scraping_interval = 180
data_path = "data/scraping"

if __name__ == "__main__":
    scraper = DailyFXScraper()
    investing_scraper = InvestingComScraper()
    reuters_scraper = ReutersComScraper()

    while True:
        print("Scraping data...")
        # scrape_dailyfx_data(scraper, data_path)
        # scrape_investor_data(investing_scraper, data_path)
        scrape_reuters_data(reuters_scraper, data_path)
        print("Done scraping data.")
        time.sleep(scraping_interval)
