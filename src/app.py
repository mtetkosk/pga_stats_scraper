import requests
import pandas as pd
from bs4 import BeautifulSoup

API_URL = "https://orchestrator.pgatour.com/graphql"
API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"
YEAR = 2023
STAT_ID = "02567"
STAT_NAME = "SG: Off-the-Tee"


# prepare the payload
payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",
        "statId": STAT_ID,
        "year": YEAR,
        "eventQuery": None
    },
    "query": "query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {\n  statDetails(\n    tourCode: $tourCode\n    statId: $statId\n    year: $year\n    eventQuery: $eventQuery\n  ) {\n    tourCode\n    year\n    displaySeason\n    statId\n    statType\n    tournamentPills {\n      tournamentId\n      displayName\n    }\n    yearPills {\n      year\n      displaySeason\n    }\n    statTitle\n    statDescription\n    tourAvg\n    lastProcessed\n    statHeaders\n    statCategories {\n      category\n      displayName\n      subCategories {\n        displayName\n        stats {\n          statId\n          statTitle\n        }\n      }\n    }\n    rows {\n      ... on StatDetailsPlayer {\n        __typename\n        playerId\n        playerName\n        country\n        countryFlag\n        rank\n        rankDiff\n        rankChangeTendency\n        stats {\n          statName\n          statValue\n          color\n        }\n      }\n      ... on StatDetailTourAvg {\n        __typename\n        displayName\n        value\n      }\n    }\n  }\n}"  
  }


# post the request
page = requests.post(API_URL, json=payload, headers={"x-api-key": API_KEY})

# check for status code
page.raise_for_status()

# get the data
data = page.json()["data"]["statDetails"]["rows"]

# format to a table that is in the webpage
table = map(lambda item: {
    "rank": item["rank"],
    "player": item["playerName"],
    STAT_NAME: item["stats"][0]["statValue"],
}, data)

# convert the dataframe
s = pd.DataFrame(table)

print(s)

s.to_csv('test.csv', index=False)