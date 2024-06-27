import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from google_maps import get_recs
# import requests
import pandas as pd
import sqlalchemy as db
# import json

load_dotenv()

zipcode = False

while not zipcode:
    x = input('''
Hello! I'm your personalized AI Assistant ready
to provide local restaurant reccomendations.
Please describe your preferences.
Firstly, what is your zip code?
'''
              )

    pattern = r"^\d{5}$"
    match = re.match(pattern, x)
    if match:
        print(match)
        zipcode = True

y = input('''
Now, please describe to me some dietary preferences.
'''
          )
""" 
# initialize client with API key from .env
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
# Starting a chat with GPT3.5
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": '''
Based off the user input, return an appropriate query\
(of 4 words or less)\
 that could be inputted into Google Maps.
The user is looking for places to eat. \
Please take into account what type of food they want.
For example, if the person inputs "meatless" \
a good query would be something like \
"vegan food near me"
'''
         },
        {"role": "user", "content": '''
        I have a preference for {y}}
        '''}],
    stream=True,
)

# regex for 5 digit zip code, /^\d{5}$/
# https://skillforge.com/how-to-use-javascript-regular-expressions/#:~:text=So%20%5E%5Cd%7B5%7D,must%20start%20with%20five%20numbers.
test = ""
for chunk in stream:
    if chunk.choices[0].delta.content:
        test += chunk.choices[0].delta.content
# ans = json.loads(test)
print(test)
"""
'''
per person
    0: Free
    1: Inexpensive (<=$10)
    2: Moderate ($10 - $25)
    3: Expensive ($25 - $45)
    4: Very Expensive (>=$45)
'''

prices = {
    "0.0": "Free",
    "1.0": "<= $10",
    "2.0": "$10 - $25",
    "3.0": "$25 - $45",
    "4.0": ">= $45"
}
engine = db.create_engine('sqlite:///restaurants.db')
ans = "y"
results = get_recs(x, y)['results']
df = pd.DataFrame.from_dict(results)
df = df.astype(str)
df['price_level'] = df['price_level'].map(prices)

df.to_sql('Reccomendations', con=engine, if_exists='replace', index=False)
vicinity_renamed = False

print("Here are the Top 5 Reccomended Restaurants near you")

with engine.connect() as connection:
    if not vicinity_renamed:
        connection.execute(db.text("ALTER TABLE Reccomendations RENAME COLUMN vicinity to address;"))
        vicinity_renamed = True
    table = connection.execute(
        db.text("SELECT name, address, rating, price_level FROM Reccomendations;")
        )
    while ans != "n":
        
        query_result = table.fetchmany(5)
        if len(query_result) == 0:
            print("There are no more reccomendations")
            break
        print(pd.DataFrame(query_result))
        print()
        ans = input("Would you like more reccomendations? (y/n): ")
        print()

print("Thank you for using INSERT NAME, I hope that you have a wonderful meal from the restaurant you chose")