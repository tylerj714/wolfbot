# bot.py
import os

import discord

from dotenv import load_dotenv

from message_manager import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(
        f'{client.user.name} has connected to Discord!\n'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_manager = MessageManager(message)

    if message.content.startswith('!wb'):
        await message_manager.manage()

client.run(TOKEN)
