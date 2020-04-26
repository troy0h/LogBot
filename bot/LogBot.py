import discord
import logging
import yaml
import aiohttp
import asyncio
from urllib.request import Request, urlopen
#logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
token = yaml.safe_load(open(r'C:\Users\joshu\Documents\GitHub\LogBot\bot\token.yml'))

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    try:
        n = len(message.attachments[0].filename)
        filenametest = message.attachments[0].filename[n-3:n]
        print(filenametest)
        if filenametest == "txt":
            url = message.attachments[0].url
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            lines = urlopen(req)
            for line in lines:
                output=line.decode('utf-8')
                
            
        else:
            return
    except IndexError:
        pass

client.run(token["token"])
