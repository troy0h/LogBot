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
yuzuEA = "https://cdn.discordapp.com/attachments/703956227280994470/703974900733575278/YuzuEA.png"
yuzuBase = "https://cdn.discordapp.com/attachments/703956227280994470/703974900733575278/Yuzu.png"
imageLocation = ""
played_games=[]

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

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
                
                if(output[61:74]=="yuzu Version:"):
                    end_index=str(output).find("| HEAD")
                    yuzu_version = output[74:end_index]
                    print(yuzu_version)
                elif(output[61:70]=="Host CPU:"):
                    cpu = output[70:]
                    print(cpu)
                elif(output[61:69]=="Host OS:"):
                    os = output[69:]
                    print(os)
                elif(output[94:101]=="Vulkan:"):
                    renderer="Vulkan"
                    print(renderer)
                elif(output[106:118]=="GL_RENDERER:"):
                    renderer="OpenGl"
                    print(renderer)
                elif(output[59:72]=="Booting game:"):
                    played_games.append(str(output[91:]).replace("\r\n",""))

                    if yuzu_version[0:17] == "yuzu Early Access":
                        imageLocation = yuzuEA
                    else:
                        imageLocation = yuzuBase

            embed = discord.Embed(title=yuzu_version,color=0x00ff00)
            embed.set_thumbnail(url=imageLocation)
            embed.add_field(name="CPU", value=cpu, inline=False)
            embed.add_field(name="GPU", value="Radeon RX 570 Series", inline=False)
            embed.add_field(name="OS", value=os, inline=False)
            embed.add_field(name="Graphics API", value=renderer, inline=False)
            await message.channel.send(embed=embed)
            
        else:
            print("skipping")
            return

    except IndexError:
        pass

client.run(token["token"])
