# message_manager.py
# manages responding to message requests

from game import *


class MessageManager:
    def __init__(self, message):
        self.message = message

    async def manage(self):
        mg_message = self.message
        if mg_message.content.startswith('!wb --game'):
            await self.game()
        if mg_message.content.startswith('!wb --round'):
            await self.round()
        if mg_message.content.startswith('!wb --vote'):
            await self.vote()
        return

    async def game(self):
        gm_msg = self.message
        if gm_msg.content.startswith('!wb --game create'):
            game = Game(gm_msg.author, gm_msg.guild)
            response = f'New game created by {game.creator.name} in server {game.guild.name} with ID {game.id}!'
            await gm_msg.channel.send(response)
        return

    async def round(self):

        return

    async def vote(self):

        return
