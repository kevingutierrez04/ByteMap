import os
from openai import OpenAI
from dotenv import load_dotenv
import re

#import requests
import pandas as pd
import sqlalchemy as db
#import json

load_dotenv()

zipcode = False

while not zipcode:
  x = input('''
          Hello! I'm your personalized AI Assistant ready to provide local restaurant 
          reccomendations. Please describe your preferences. Firstly, what is your
          zip code?
          '''
)
  pattern = r"^\d{5}$"
  match = re.match(pattern, x)
  if match:
    print(match)
    zipcode = True

y = input('''
          Now, please describe to me some dietary preferences.
          ''')

#initialize client with API key from .env
client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY'),
)
#Starting a chat with GPT3.5
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": '''
       Based off the user input, return an appropriate query (of 4 words or less) 
       that could be inputted into Google Maps. The user is looking for places to eat.
       Please take into account what type of food they want. For example, if the person
       mentions that they're vegan, a good query would be something like "vegan food
       near me.
       '''},
      {"role": "user", "content": '''
    I have a preference for {y}}
    '''}],
    
    stream=True,
)

#regex for 5 digit zip code, /^\d{5}$/
#https://skillforge.com/how-to-use-javascript-regular-expressions/#:~:text=So%20%5E%5Cd%7B5%7D,must%20start%20with%20five%20numbers.
test = ""
for chunk in stream:
  if chunk.choices[0].delta.content:
    test += chunk.choices[0].delta.content
#ans = json.loads(test)
print(test)


location_results = {"Burgers": ["Burger King", "McDonalds", "Local Diner", "Wendy's"]}
df = pd.DataFrame.from_dict(location_results)
engine = db.create_engine('sqlite:///resturants.db')

df.to_sql('Reccomendations', con=engine, if_exists='replace', index=False)

with engine.connect() as connection:
  query_result = connection.execute(db.text("SELECT * FROM Reccomendations;")).fetchall()
  print(pd.DataFrame(query_result))







#old logic for formatting into JSON properly
#for key in ans:
#  if isinstance(ans[key], list):
#    ans[key] = '. '.join([str(item) for item in ans[key]])

#takes in dict
#epic = pd.DataFrame.from_dict([ans])

#creates db
#engine = db.create_engine('sqlite:///placeholder.db')

#converts to sql
#epic.to_sql('Responses', con=engine, if_exists='replace', index=False)

#for loop while engine is active, performs query, prints result
#with engine.connect() as connection:
#  query_result = connection.execute(db.text("SELECT * FROM Responses;")).fetchall()
#  print(pd.DataFrame(query_result))
#  print(chunk.choices[0].delta.content, end="")