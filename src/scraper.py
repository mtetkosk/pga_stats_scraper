import requests
import pandas as pd

API_URL = "https://orchestrator.pgatour.com/graphql"
API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"

class Scraper:

    @staticmethod
    def _build_payload(stat_id, year):
        return {"operationName": "StatDetails",
                "variables": {
                    "tourCode": "R",
                    "statId": stat_id,
                    "year": year,
                    "eventQuery": None
                    },
                "query": "query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {\n  statDetails(\n    tourCode: $tourCode\n    statId: $statId\n    year: $year\n    eventQuery: $eventQuery\n  ) {\n    tourCode\n    year\n    displaySeason\n    statId\n    statType\n    tournamentPills {\n      tournamentId\n      displayName\n    }\n    yearPills {\n      year\n      displaySeason\n    }\n    statTitle\n    statDescription\n    tourAvg\n    lastProcessed\n    statHeaders\n    statCategories {\n      category\n      displayName\n      subCategories {\n        displayName\n        stats {\n          statId\n          statTitle\n        }\n      }\n    }\n    rows {\n      ... on StatDetailsPlayer {\n        __typename\n        playerId\n        playerName\n        country\n        countryFlag\n        rank\n        rankDiff\n        rankChangeTendency\n        stats {\n          statName\n          statValue\n          color\n        }\n      }\n      ... on StatDetailTourAvg {\n        __typename\n        displayName\n        value\n      }\n    }\n  }\n}"  
            } 
        
    def scrape(self, stat_id, stat_name, year=2023, api_key=API_KEY):

        print(f'Scraping for stat: {stat_name}')
        # Build Payload

        payload = self._build_payload(stat_id, year)
        # post the request
        page = requests.post(API_URL, json=payload, headers={"x-api-key": API_KEY})

        # check for status code
        try:
            page.raise_for_status()
        except Exception as e:
            print(f'Web-Request Error: {e}')
            print('You may need to refresh your API key')

        # get the data
        data = page.json()["data"]["statDetails"]["rows"]

        # format to a table that is in the webpage
        data = [x for x in data if "rank" in x]
        
        table = map(lambda item: {
            f"rank_{stat_name}": item.get("rank"),
            "player": item.get("playerName"),
            stat_name: item.get("stats")[0].get("statValue"),
        }, data)


        # convert the dataframe
        try:
            s = pd.DataFrame(table)
        except Exception as e:
            print(data)
            raise(e)

        print(f'Successfully scraped stat: {stat_name}')
        print('-'* 25)
        return s