# message_manager.py
# manages responding to message requests

from wolfbot_dom import *
from discord import Reaction, User, Guild, Client, Message
from db_manager import DBManager
import db_constants
import asyncio


class MessageManager:
    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def manage(self):
        mg_message = self.message
        if mg_message.content.startswith('!wb -game'):
            await self.game()
        if mg_message.content.startswith('!wb -round'):
            await self.round()
        if mg_message.content.startswith('!wb -vote'):
            await self.vote()
        if mg_message.content.startswith('!wb -player'):
            await self.player()
        return

    async def game(self):
        gm_msg = self.message
        dbmgr = DBManager(db_constants.WOLFBOT_DB)
        if gm_msg.content.startswith('!wb -game create'):
            # Check to see if this user is already registered in the DB, if not, they need to be added
            message_player = dbmgr.get_player(gm_msg.guild, gm_msg.author)
            if message_player is None:
                response = f'Player {gm_msg.author.display_name} not registered on this server; registering player...'
                await gm_msg.channel.send(response)
                message_player = dbmgr.create_player(gm_msg.guild, gm_msg.author)
                response2 = f'Registered player {message_player.player_name}!'
                await gm_msg.channel.send(response2)

            # Check to see if there is already an active game
            current_game = dbmgr.get_current_game(gm_msg.guild)
            # If there is no currently active game, create one
            if current_game is None:
                game = dbmgr.create_game(gm_msg.guild, gm_msg.author, message_player.player_id)
                response = f'New game created by {gm_msg.author.display_name} in server {gm_msg.guild.name} with ID {game.game_id}!'
                await gm_msg.channel.send(response)
            else:
                game_creator = dbmgr.get_player_by_user_id(gm_msg.guild, current_game.creator_discord_id)
                response = f'There is already an active game created by player {game_creator.player_name} in server {gm_msg.guild.name}; ' \
                           f'the currently active game must be ended before a new one can be created.'
                await gm_msg.channel.send(response)
        elif gm_msg.content.startswith('!wb -game end'):
            current_game = dbmgr.get_current_game(gm_msg.guild)
            if current_game is None:
                response = f'No currently active game found on this server to end!'
                await gm_msg.channel.send(response)
            else:
                response = f'Are you sure you would like to end the currently active game? (👍/👎)'
                bot_msg = await gm_msg.channel.send(response)
                confirmation_result = await self.confirmation_check(client=self.client, message=bot_msg)
                if confirmation_result:
                    dbmgr.end_game(guild=gm_msg.guild, game_id=current_game.game_id)
                    response = f'Ended game {current_game.game_id} on {gm_msg.guild.name}'
                    await gm_msg.channel.send(response)
                else:
                    response = f'Cancelled ending the currently active game on {gm_msg.guild.name}'
                    await gm_msg.channel.send(response)
        dbmgr.connection.close()
        return

    async def round(self):

        return

    async def vote(self):

        return

    async def player(self):

        return

    async def confirmation_check(self, client: Client, message: Message) -> bool:

        def thumb_check(check_reaction, check_user):
            return str(check_reaction.emoji) in ['👍', '👎'] and check_user != client.user and check_reaction.message == message

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=thumb_check)
        except asyncio.TimeoutError:
            await message.channel.send("Response not confirmed in time; please try again")
        else:
            if str(reaction.emoji) == '👍':
                return True
            elif str(reaction.emoji) == '👎':
                return False
            else:
                return False
