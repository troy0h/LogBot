import discord
import token

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello')
        await message.channel.send('Hello!')
        

token.clientrun()
