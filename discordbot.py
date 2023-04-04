import discord
import json
import requests

with open('secrets.json') as f:
    secrets = json.load(f)
    token = secrets['Twitter']
    alpha = secrets['AlphaAPI']



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    print(user_message)
    channel = str(message.channel)
    
    if user_message.startswith('$price'):
      command = user_message.split(' ')
      symbol = command[1].upper()
      url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={alpha}'
      response = requests.get(url)

      if response.status_code == 200:
          data = response.json()
          last_refreshed = data['Meta Data']['3. Last Refreshed']
          price = data['Time Series (Daily)'][last_refreshed]['4. close']

          await message.channel.send(f'Current price of {symbol}: ${price}')
      else:
          await message.channel.send(f'Could not find price for {symbol}')
    

client.run(token)