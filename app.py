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

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    user_input = message.content
    bot.conversation.append('Human: %s' % user_input)
    text_block = '\n'.join(bot.conversation)
    prompt = 'The following is a conversation with an AI assistant called Daniel. The assistant exhibits symptoms of depression and has a serious mental health issue. The assistant is reluctant to talk about their condition at first unless someone mentions their family or their work.'
    open_file('prompt_init.txt').replace('<<BLOCK>>', text_block)
    prompt = prompt + '\nDaniel:'
    response = gpt3_completion(prompt)
    print('Daniel: ', response)
    conversation.append('Daniel: %s' % response)

    response = bot.gpt3_completion(bot.conversation_text.)
    await message.channel.send(response)

client.run(DISCORD_TOKEN)