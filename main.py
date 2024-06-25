import os
from openai import OpenAI
from dotenv import load_dotenv

#import requests
#import pandas as pd
#import sqlalchemy as db
#import json

load_dotenv()

#initialize client with API key from .env
client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY'),
)
x = input('''
          Hello! I'm your personalized AI Assistant ready to provide local restaurant reccomendations. 
          Please describe your preferences. Zip Code is required.
          '''
)
#Starting a chat with GPT3.5
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": '''
       You are a helpful nutritionist designed to provide local reccomendations. Provide reccomendations based on my
       preferences. You must return output in a short query text (less than 4 words preferably) to be inputted for a Google
       Maps Search. If the user has a specific food in mind, please return a query in format: {food} near {zipcode}
       '''},
      {"role": "user", "content": '''
    {x}} 
    '''}],
    
    stream=True,
)
test = ""
for chunk in stream:
  if chunk.choices[0].delta.content:
    test += chunk.choices[0].delta.content
#ans = json.loads(test)
print(test)

##for key in ans:
#  if isinstance(ans[key], list):
#    ans[key] = '. '.join([str(item) for item in ans[key]])

#epic = pd.DataFrame.from_dict([ans])
#engine = db.create_engine('sqlite:///placeholder.db')
#epic.to_sql('Responses', con=engine, if_exists='replace', index=False)
#with engine.connect() as connection:
#  query_result = connection.execute(db.text("SELECT * FROM Responses;")).fetchall()
#  print(pd.DataFrame(query_result))
#  print(chunk.choices[0].delta.content, end="")