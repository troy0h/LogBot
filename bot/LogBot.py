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
token = yaml.safe_load(open('token.yml'))


played_games=[]
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    try:
        n = len(message.attachments[0].filename)
        filenametest = message.attachments[0].filename[n-3:n]
        
        if filenametest == "txt":
            played_games.clear()
            url = message.attachments[0].url
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            lines = urlopen(req)
            for line in lines:
                output=line.decode('utf-8')
                
                if(output[61:74]=="yuzu Version:"):
                    end_index=str(output).find("| HEAD")
                    yuzu_version = output[74:end_index]
                elif(output[61:70]=="Host CPU:"):
                    cpu = output[70:]
                elif(output[61:69]=="Host OS:"):
                    os = output[69:]
                elif(output[94:101]=="Device:"):
                    renderer="Vulkan"
                    gpu=output[102:]
                  
                elif(output[106:118]=="GL_RENDERER:"):
                    renderer="OpenGl"
                    gpu=output[119:]
                   

                elif(output[59:72]=="Booting game:"):
                    played_games.append(str(output[91:]).replace("\r\n",""))
            isEA=False
            embed = discord.Embed(
            title=yuzu_version,
            description="Desc",
            color=0x00ff00)
            for i in str(yuzu_version).split():
                if i=="Early":
                    RealImageLocation="https://github.com/troy0h/LogBot/raw/master/bot/Logos/YuzuEA.png"
                    isEA=True
            if isEA==False:
                RealImageLocation="https://github.com/troy0h/LogBot/raw/master/bot/Logos/Yuzu.png"
            embed.set_thumbnail(url=RealImageLocation)
            embed.add_field(name="CPU", value=cpu, inline=False)
            embed.add_field(name="GPU", value=gpu, inline=False)
            embed.add_field(name="OS", value=os, inline=False)
            embed.add_field(name="Graphics API", value=renderer, inline=False)
            if(len(played_games)>0):
                embed.add_field(name="Last Played Game", value=played_games[len(played_games)-1], inline=False)
            await message.channel.send(embed=embed)
                    

    except IndexError:
        pass


client.run(token["token"])
