from dotenv import load_dotenv
import re
from google_maps import get_recs
# import requests
import pandas as pd
import sqlalchemy as db
# import json

load_dotenv()


def getInput():

    zipcode = False

    while not zipcode:
        x = input('''
Hello! Welcome to ByteMap. I'm your personalized assistant ready
to provide local restaurant reccomendations.
Please describe your preferences.
Firstly, what is your zip code?
'''
                  )

        pattern = r"^\d{5}$"
        match = re.match(pattern, x)
        if match:
            # print(match)
            zipcode = True

    y = input('''
Now, please describe to me some dietary preferences.
'''
              )
    sorting = input("Would you like the results sorted by "
                    "Prominence (Default), distance, or ratings?: ")
    return x, y, sorting.lower()


def printResults(zipcode, food, sort):
    prices = {
        "0.0": "Free",
        "1.0": "<= $10",
        "2.0": "$10 - $25",
        "3.0": "$25 - $45",
        "4.0": ">= $45",
        'nan': "Prices Unavailable"
    }
    engine = db.create_engine('sqlite:///restaurants.db')

    if sort == "":
        sort = "prominence"

    if sort == "ratings":
        results = get_recs(zipcode, food)['results']
    else:
        results = get_recs(zipcode, food, sort)['results']

    df = pd.DataFrame.from_dict(results)
    df = df.astype(str)
    df['price_level'] = df['price_level'].map(prices)

    df.to_sql('Reccomendations', con=engine, if_exists='replace', index=False)
    vicinity_renamed = False

    print("Here are the Top 5 Reccomended Restaurants near you")

    with engine.connect() as connection:
        if not vicinity_renamed:
            connection.execute(db.text("ALTER TABLE Reccomendations "
                                       "RENAME COLUMN vicinity to address;"))
            vicinity_renamed = True
        if sort == "ratings":
            table = connection.execute(
                db.text("SELECT name, address, rating, "
                        "price_level FROM Reccomendations "
                        "ORDER BY rating DESC;")
                )
        else:
            table = connection.execute(
                db.text("SELECT name, address, rating, "
                        "price_level FROM Reccomendations;")
                )
        ans = "y"
        while ans != "n" and ans != "no":
            query_result = table.fetchmany(5)
            if len(query_result) == 0:
                print("There are no more reccomendations")
                break
            print(pd.DataFrame(query_result))
            print()
            ans = input("Would you like more reccomendations? (y/n): ")
            ans = ans.lower()
            print()

if __name__ == "__main__":
    zipcode, food, sort = getInput()
    printResults(zipcode, food, sort)
    print("Thank you for using ByteMap, I hope "
          "that you have a wonderful meal from the "
          "restaurant you chose")
