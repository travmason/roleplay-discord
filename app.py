# bot.py
import os
import logging
import logging.handlers
import discord
from dotenv import load_dotenv
import random
from website.daniel import Bot  

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.WARNING)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

consolehandler = logging.StreamHandler()
consolehandler.setFormatter(formatter)
logger.addHandler(consolehandler)

logger.info('logging started')

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

client.run(DISCORD_TOKEN, log_handler=None)
