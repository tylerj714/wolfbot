# bot.py
import os

import discord

from dotenv import load_dotenv
from logging_manager import logger

from message_manager import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BASE_PATH = os.getenv('BASE_PATH')

client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_manager = MessageManager(client, message)

    if message.content.startswith('!wb'):
        await message_manager.manage()

client.run(TOKEN)
