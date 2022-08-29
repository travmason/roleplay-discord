# bot.py
import os
import logging
import discord
from dotenv import load_dotenv
import random
from website.daniel import Bot  

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())
bot = Bot()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})\n')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content
    bot.conversation_text.append('Human: %s' % user_input)
    text_block = '\n'.join(bot.conversation_text)
    prompt = 'The following is a conversation with an AI assistant called Daniel. The assistant exhibits symptoms of depression and has a serious mental health issue. The assistant is reluctant to talk about their condition at first unless someone mentions their family or their work.'
    #open_file('prompt_init.txt').replace('<<BLOCK>>', text_block)
    prompt = prompt + '\n' + text_block + '\nDaniel:'
    print('prompt before gpt3 is :' + prompt)
    response = bot.gpt3_completion(prompt)
    bot.conversation_text.append('Daniel: %s' % response)

    await message.channel.send(response)

client.run(DISCORD_TOKEN)
