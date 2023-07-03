from fire import Fire
import pandas as pd
from scraper import Scraper

web_scraper = Scraper()

YEAR = 2023
STAT_ID = "02567"
STAT_NAME = "SG: Off-the-Tee"

STATS = {}

STATS_CONFIG = {"02567": "SG: Off-the-Tee",
                "02675": "SG: Total",
                "02674": "SG: Tee-to-Green",
                "02568": "SG: Approach the Green",
                "02569": "SG: Around-the-Green",
                "02564": "SG: Putting",
                "120": "Scoring Average",
                "101": "Driving Distance",
                "103": "GIR Percentage",
                "130": "Scrambling",
                }

def main(year=2023):
    master = pd.DataFrame()
    for stat_id in STATS_CONFIG:
        stats = web_scraper.scrape(stat_id, STATS_CONFIG[stat_id])
        if len(master) == 0:
            master = stats
        else:
            master = pd.merge(master, stats, on='player')
    
    master.to_csv('stats.csv', index=False)
    print('Wrote stats to csv!')

if __name__ == '__main__':
    Fire(main)