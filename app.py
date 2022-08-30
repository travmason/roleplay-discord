# bot.py
import os
import logging
import discord
from dotenv import load_dotenv
import random
from website.daniel import Bot  

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(filename='discord.log', level=logging.INFO)

client = discord.Client(intents=discord.Intents.default())
bot = Bot()

@client.event
async def on_ready():
    logging.info('%s has connected to Discord!', client.user)
    for guild in client.guilds:
        logging.info('%s (id: %s)\n', guild.name, guild.id)

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
    logging.info('Prompt: ' + prompt)
    response = bot.gpt3_completion(prompt)
    bot.conversation_text.append('Daniel: %s' % response)
#    logging.info('\n'.join(map(str, bot.conversation_text)))

    await message.channel.send(response)

client.run(DISCORD_TOKEN)
