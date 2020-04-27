import os
try:
    import discord
except:
    os.system("py -m pip install discord.py")
    os.system("py -m pip install PyYAML")
    input("Please restart the program, press anything to quit")
import logging
try:
    import yaml
except:
    os.system("py -m pip install discord.py")
    os.system("py -m pip install PyYAML")
    input("Please restart the program, press anything to quit")
import aiohttp
import asyncio
from urllib.request import Request, urlopen


#logging
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

client = discord.Client()
token = yaml.safe_load(open(os.path.abspath(os.getcwd())+r'\bot\token.yml'))

strings_errors=yaml.safe_load(open(os.path.abspath(os.getcwd())+r'\bot\error_messages.yml'))

played_games=[]
errors=[]
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!restart_log_bot'):
        await message.channel.send('Restarting, please wait')
        import os
        os.system("py "+os.path.dirname(os.path.abspath(__file__))+"\LogBot.py restart")
        print("quitting")
        quit()
            
            
        return
    try:
        n = len(message.attachments[0].filename)
        filenametest = message.attachments[0].filename[n-3:n]
        print(filenametest)
        if filenametest == "txt":
            errors.clear()
            played_games.clear()
            url = message.attachments[0].url
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            lines = urlopen(req)
            aSync=None
            boxcat=None
            docked=None
            gpu="Please start a game"
            renderer="Please start a game"
            for line in lines:
                line=line.replace(b'\r\n',b'')
                output=line.decode('utf-8')
                
                if(output[61:74]=="yuzu Version:"):
                    end_index=str(output).find("| HEAD")
                    yuzu_version = output[74:end_index]
                if output[9:]=="Debug <Critical> yuzu\main.cpp:OnGameListOpenFolder:1154: Assertion Failed! Game uses both user and device savedata?":
                    errors.append(strings_errors["assertion"])
                elif(output[61:70]=="Host CPU:"):
                    cpu = output[70:]
                   
                elif(output[61:69]=="Host OS:"):
                    os = output[69:]
                
                elif(output[94:101]=="Device:"):
                        renderer="Vulkan"
                        gpu=output[102:]
                
                elif(output[106:118]=="GL_RENDERER:"):
                        renderer="OpenGL"
                        gpu=output[119:]
            
                    
                elif(output[61:99]=="Renderer_UseAsynchronousGpuEmulation: "):
      
              
                    if(output[99:]=="false"):
                        aSync=False
                    else:
                        aSync=True
                elif(output[61:83]=="System_UseDockedMode: "):
                    
                    if(output[83:]=="false"):
                        docked=False
                    else:
                        docked=True
                
                elif(output[61:83]=="Services_BCATBackend: "):
                    
                    if(output[83:]=="none"):
                        boxcat=False
                    else:
                        boxcat=True
                elif(output[59:72]=="Booting game:"):
                    played_games.append(str(output[92:]).replace("\r\n",""))
            #rules
            try:
                if (gpu[:6]=="Radeon"):
                    if (renderer=="OpenGL"):
                        errors.append(strings_errors["opengl+amd"])
            except:
                print("Cant find error in log")
            
            if(aSync==False):
                errors.append(strings_errors["async"])
            if(boxcat==True):
                errors.append(strings_errors["boxcat"])
            isEA=False

            embed = discord.Embed(
            title=str(yuzu_version).replace("yuzu","Yuzu"),
            description="",
            color=0x00ff00)
            for i in str(yuzu_version).split():
                if i=="Early":
                    RealImageLocation="https://github.com/troy0h/LogBot/raw/master/bot/Logos/YuzuEA.png"
                    isEA=True
            if isEA==False:
                RealImageLocation="https://github.com/troy0h/LogBot/raw/master/bot/Logos/Yuzu.png"
            if renderer=="Vulkan":
                print("Found Vulkan!")
                for i in played_games:
                    
                    if i=="Animal Crossing: New Horizons":
                        errors.append(strings_errors["acnh+vulkan"])
            embed.set_thumbnail(url=RealImageLocation)
            
            embed.add_field(name="CPU", value=cpu, inline=False)
            embed.add_field(name="GPU", value=gpu, inline=False)
            embed.add_field(name="OS", value=os, inline=True)
            embed.add_field(name="Graphics API", value=renderer, inline=True)
            embed.add_field(name="Docked", value=docked, inline=True)
            if(len(played_games)>0):
                embed.add_field(name="Last Played Game", value=played_games[len(played_games)-1], inline=False)
            for i in range(0,len(errors)):
                if i==0:
                    embed.add_field(name="Warning: ", value=errors[i], inline=False)
                else:
                    embed.add_field(name="Warning: ", value=errors[i], inline=True)
            await message.channel.send(embed=embed)
                    

    except IndexError:
        pass

client.run(token["token"])
