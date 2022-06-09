# message_manager.py
# manages responding to message requests
from typing import List

from wolfbot_dom import *
from discord import Reaction, User, Guild, Client, Message, Member, TextChannel
from db_manager import DBManager
import db_constants
import asyncio
from logging_manager import logger
import time
import re


class MessageManager:
    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def manage(self):
        mg_message = self.message
        logger.info(f'Got message {mg_message.content} from {mg_message.guild.id} in channel {mg_message.channel.name}')
        if mg_message.content.startswith('!wb -game'):
            await self.game()
        if mg_message.content.startswith('!wb -round'):
            await self.round()
        if mg_message.content.startswith('!wb -vote'):
            await self.vote()
        if mg_message.content.startswith('!wb -player'):
            await self.player()

        logger.info(
            f'Finished with actions for message {mg_message.content} from {mg_message.guild.id} in channel {mg_message.channel.name}')

        return

    async def help(self):

        return

    async def game(self):
        gm_msg = self.message
        dbmgr = DBManager(db_constants.WOLFBOT_DB)

        # Create the game
        if gm_msg.content.startswith('!wb -game create'):
            # Verify this user is registered; if they are not, register them
            player_list = await self.register_players(dbmgr, gm_msg.channel, [gm_msg.author], gm_msg.guild)

            # Check to see if there is already an active game
            current_game = dbmgr.get_current_game(gm_msg.guild)
            # If there is no currently active game, create one
            if current_game is None:
                response = f'Creating a new game in server {gm_msg.guild.name}...'
                logger.info(f'sending response: {response}')
                bot_msg = await gm_msg.channel.send(response)
                dbmgr.create_game(gm_msg.guild, gm_msg.author, player_list[0].player_id)
                updated_response = response + " and it's done! :tada: Have fun!"
                logger.info(f'editing response: {updated_response}')
                await bot_msg.edit(content=updated_response)
            else:
                game_creator = dbmgr.get_player_by_user_id(gm_msg.guild, current_game.creator_discord_id)
                response = f'There is already an active game created by player {game_creator.player_name} in server {gm_msg.guild.name}; ' \
                           f'the currently active game must be ended before a new one can be created.'
                logger.info(f'sending response: {response}')
                await gm_msg.channel.send(response)

        # End the game
        elif gm_msg.content.startswith('!wb -game end'):
            current_game = dbmgr.get_current_game(gm_msg.guild)
            if current_game is None:
                response = f'No currently active game found on this server to end!'
                logger.info(f'sending response: {response}')
                await gm_msg.channel.send(response)
            else:
                response = f'Are you sure you would like to end the currently active game? (:+1:/:-1:)'
                logger.info(f'sending response: {response}')
                bot_msg = await gm_msg.channel.send(response)
                confirmation_result = await self.confirmation_check(client=self.client, message=bot_msg)
                if confirmation_result:
                    dbmgr.end_game(guild=gm_msg.guild, game_id=current_game.game_id)
                    response2 = f'Ended game {current_game.game_id} on {gm_msg.guild.name}'
                    logger.info(f'sending response: {response2}')
                    await gm_msg.channel.send(response2)
                else:
                    response2 = f'Cancelled ending the currently active game on {gm_msg.guild.name}'
                    logger.info(f'sending response: {response2}')
                    await gm_msg.channel.send(response2)

        # Add player to game
        elif gm_msg.content.startswith('!wb -game add-player'):
            # Make sure the player submitting the request has been registered
            msg_player = await self.get_message_author_as_player(dbmgr=dbmgr, channel=gm_msg.channel,
                                                                 user=gm_msg.author, guild=gm_msg.guild)
            # First, make sure all players are registered
            player_list = await self.register_players(dbmgr, gm_msg.channel, gm_msg.mentions, gm_msg.guild)
            # Second, make sure there's even a game created that is active on this server
            current_game = await self.get_current_game_with_create(player=msg_player, message=gm_msg,
                                                                   guild=gm_msg.guild, dbmgr=dbmgr)
            # Finally, add all the players to the game
            await self.add_players_to_game(dbmgr=dbmgr, channel=gm_msg.channel, game=current_game, players=player_list)

        dbmgr.connection.close()
        return

    async def get_current_game(self, message: Message, guild: Guild, dbmgr: DBManager) -> Game:
        current_game = dbmgr.get_current_game(guild)
        if current_game is None:
            response = f'I didn\'t find an active game on this server.'
            logger.info(f'sending response: {response}')
            await message.channel.send(response)
        else:
            response = f'Found an active game on this server! (It was hidden under an old wolf treat box)'
            logger.info(f'sending responses: {response}')
            await message.channel.send(response)
        return current_game

    async def get_current_game_with_create(self, player: Player, message: Message, guild: Guild,
                                           dbmgr: DBManager) -> Game:
        current_game = dbmgr.get_current_game(guild)
        if current_game is None:
            response = f'I didn\'t find an active game on this server, would you like to start one? (:+1:/:-1:)'
            logger.info(f'sending response: {response}')
            bot_msg = await message.channel.send(response)
            confirmation_result = await self.confirmation_check(client=self.client, message=bot_msg)
            if confirmation_result:
                current_game = dbmgr.create_game(guild, message.author, player.player_id)
                updated_response = response + " Alright then, got you covered! :tada: Have fun!"
                logger.info(f'editing response: {updated_response}')
                await bot_msg.edit(content=updated_response)
            else:
                response2 = f'Okay, that\'s fine. Maybe another time. :shrug:'
                logger.info(f'sending response: {response2}')
                await message.channel.send(response2)
                return None
        else:
            response = f'Found an active game on this server! (It was hidden under an old wolf treat box)'
            logger.info(f'sending responses: {response}')
            await message.channel.send(response)
        return current_game

    async def round(self):

        return

    async def vote(self):

        return

    async def player(self):
        ply_msg = self.message
        dbmgr = DBManager(db_constants.WOLFBOT_DB)
        if ply_msg.content.startswith('!wb -player register'):
            await self.register_players(dbmgr, ply_msg.channel, ply_msg.mentions, ply_msg.guild)
        elif ply_msg.content.startswith('!wb -player resurrect'):
            msg_player = await self.get_message_author_as_player(dbmgr=dbmgr, channel=ply_msg.channel,
                                                                 user=ply_msg.author, guild=ply_msg.guild)
            current_game = await self.get_current_game(message=ply_msg, guild=ply_msg.guild, dbmgr=dbmgr)
            if msg_player.player_id == current_game.creator_player_id:
                # get the mentioned player(s) from the game, and update their status to killed
                player_list = await self.update_player_game_status(dbmgr=dbmgr, game=current_game,
                                                                   channel=ply_msg.channel,
                                                                   users=ply_msg.mentions, guild=ply_msg.guild,
                                                                   status=db_constants.PLAYER_ALIVE)
            else:
                await self.not_game_creator_message(dbmgr=dbmgr, user=ply_msg.author, game=current_game,
                                                    guild=ply_msg.guild,
                                                    channel=ply_msg.channel)
        elif ply_msg.content.startswith('!wb -player kill'):
            msg_player = await self.get_message_author_as_player(dbmgr=dbmgr, channel=ply_msg.channel,
                                                                 user=ply_msg.author, guild=ply_msg.guild)
            current_game = await self.get_current_game(message=ply_msg, guild=ply_msg.guild, dbmgr=dbmgr)
            if msg_player.player_id == current_game.creator_player_id:
                # get the mentioned player(s) from the game, and update their status to killed
                player_list = await self.update_player_game_status(dbmgr=dbmgr, game=current_game,
                                                                   channel=ply_msg.channel,
                                                                   users=ply_msg.mentions, guild=ply_msg.guild,
                                                                   status=db_constants.PLAYER_DEAD)
            else:
                await self.not_game_creator_message(dbmgr=dbmgr, user=ply_msg.author, game=current_game,
                                                    guild=ply_msg.guild,
                                                    channel=ply_msg.channel)
        elif ply_msg.content.startswith('!wb -player replace'):
            msg_player = await self.get_message_author_as_player(dbmgr=dbmgr, channel=ply_msg.channel,
                                                                 user=ply_msg.author, guild=ply_msg.guild)
            current_game = await self.get_current_game(message=ply_msg, guild=ply_msg.guild, dbmgr=dbmgr)
            if msg_player.player_id == current_game.creator_player_id:
                # get the first and second mentioned players, and update the replacement
                msg_search = re.search(r'<@(\d+)>\s+with\s+<@(\d+)>', ply_msg.content)
                if len(msg_search.groups()) == 2:
                    logger.info(f'mention 1 group is: {msg_search.group(1)} and mention 2 group is: {msg_search.group(2)}')
                    replaced_user = await self.client.fetch_user(msg_search.group(1))
                    replacing_user = await self.client.fetch_user(msg_search.group(2))
                    logger.info(f'got replaced_user {replaced_user.id} {replaced_user.display_name} and replacing_user {replacing_user.id} {replacing_user.display_name}')

                    if replaced_user is not None and replacing_user is not None:
                        await self.replace_player(dbmgr=dbmgr, channel=ply_msg.channel, replaced_user=replaced_user,
                                                  replacing_user=replacing_user,
                                                  guild=ply_msg.guild, game=current_game)
                else:
                    response = f'Invalid request format; expected request format is:\n' \
                               f'!wb -player replace <@mentioned-player> with <@mentioned-player>'
                    logger.info(f'sending response: {response}')
                    await ply_msg.channel.send(response)
            else:
                await self.not_game_creator_message(dbmgr=dbmgr, user=ply_msg.author, game=current_game,
                                                    guild=ply_msg.guild,
                                                    channel=ply_msg.channel)

        dbmgr.connection.close()
        return

    async def replace_player(self, dbmgr: DBManager, channel: TextChannel, replaced_user: User, replacing_user: User,
                             guild: Guild, game: Game):
        replaced_player = dbmgr.get_player(guild, replaced_user)
        replacing_player = dbmgr.get_player(guild, replacing_user)

        #TODO Need to verify that both players are currently register, and exist in the active game or some weird stuff will happen

        dbmgr.replace_player(game, replaced_player, replacing_player)

        response = f'Player ~~{replaced_player.player_name}~~ has been replaced by player {replacing_player.player_name}!'
        logger.info(f'sending response: {response}')
        await channel.send(response)

    async def update_player_game_status(self, dbmgr: DBManager, channel: TextChannel, users: List[User], guild: Guild,
                                        game: Game, status: str) -> List[Player]:
        player_list = dbmgr.get_players_in_game(guild=guild, game=game)

        for user in users:
            was_updated = False
            for player in player_list:
                logger.info(f'Comparing {user.id} to {player.player_discord_id}')
                if str(user.id) == player.player_discord_id:
                    dbmgr.update_player_status(status=status, game=game, player=player)
                    was_updated = True
                    response = f'Player {user.display_name} has had their status updated to {status}'
                    logger.info(f'sending response: {response}')
                    bot_msg = await channel.send(response)
                    break
            if not was_updated:
                response = f'Failed to update status for player {user.display_name} to {status}'
                logger.info(f'sending response: {response}')
                bot_msg = await channel.send(response)
        return player_list

    async def get_message_author_as_player(self, dbmgr: DBManager, channel: TextChannel, user: User,
                                           guild: Guild) -> Player:
        user_player = dbmgr.get_player(guild, user)
        if user_player is None:
            response = f'Player {user.display_name} not registered on this server; registering player...'
            logger.info(f'sending response: {response}')
            bot_msg = await channel.send(response)
            user_player = dbmgr.create_player(guild, user)
            updated_response = response + " fixed it! :+1:"
            logger.info(f'editing response: {updated_response}')
            await bot_msg.edit(content=updated_response)
        elif user_player is not None and user_player.player_name != user.display_name:
            response = f'Player name {user_player.player_name} has changed since last registered; ' \
                       f'updating name to {user.display_name}...'
            logger.info(f'sending response: {response}')
            bot_msg = await channel.send(response)
            user_player = dbmgr.update_player_name(user_player.player_id, guild, user)
            updated_response = response + " fixed it! :+1:"
            logger.info(f'editing response: {updated_response}')
            await bot_msg.edit(content=updated_response)
        return user_player

    async def register_players(self, dbmgr: DBManager, channel: TextChannel, users: List[User], guild: Guild) -> List[Player]:
        player_list = []

        if len(users) > 0:
            for user in users:
                # Check to see if this user is already registered in the DB, if not, they will be added
                user_player = dbmgr.get_player(guild, user)
                if user_player is None:
                    response = f'Player {user.display_name} not registered on this server; registering player...'
                    logger.info(f'sending response: {response}')
                    bot_msg = await channel.send(response)
                    created_player = dbmgr.create_player(guild, user)
                    updated_response = response + " fixed it! :+1:"
                    logger.info(f'editing response: {updated_response}')
                    await bot_msg.edit(content=updated_response)
                    player_list.append(created_player)
                elif user_player is not None and user_player.player_name != user.display_name:
                    response = f'Player name {user_player.player_name} has changed since last registered; ' \
                               f'updating name to {user.display_name}...'
                    logger.info(f'sending response: {response}')
                    bot_msg = await channel.send(response)
                    updated_player = dbmgr.update_player_name(user_player.player_id, guild, user)
                    updated_response = response + " fixed it! :+1:"
                    logger.info(f'editing response: {updated_response}')
                    await bot_msg.edit(content=updated_response)
                    player_list.append(updated_player)
                else:
                    response = f'Player {user_player.player_name} is already registered on this server!'
                    logger.info(f'sending response: {response}')
                    await channel.send(response)
                    player_list.append(user_player)
        return player_list

    async def add_players_to_game(self, dbmgr: DBManager, channel: TextChannel, game: Game, players: List[Player]):
        for player in players:
            game_player = dbmgr.get_game_player(game, player)
            if game_player is None:
                response = f'Adding {player.player_name} to the active game...'
                logger.info(f'sending response: {response}')
                bot_msg = await channel.send(response)
                dbmgr.add_player_to_game(game, player)
                updated_response = response + "and they're ready to play! :tada:"
                logger.info(f'editing response: {updated_response}')
                await bot_msg.edit(content=updated_response)
            else:
                response = f'Well this is embarassing...{player.player_name} is already part of this game!'
                logger.info(f'sending response: {response}')
                await channel.send(response)
        return

    async def not_game_creator_message(self, dbmgr: DBManager, game: Game, guild: Guild, user: User,
                                       channel: TextChannel):
        player = dbmgr.get_player_by_user_id(guild=guild, user_id=game.creator_discord_id)
        response = f'Hey {user.display_name}, who do you think you are? You\'re not the moderator! ' \
                   f'Only {player.player_name} can do that!'
        logger.info(f'sending response: {response}')
        await channel.send(response)

    async def confirmation_check(self, client: Client, message: Message) -> bool:

        def thumb_check(check_reaction, check_user):
            return str(check_reaction.emoji) in ['👍', '👎'] \
                   and check_user != client.user \
                   and check_reaction.message == message

        try:
            logger.info(f'Awaiting response...')
            reaction, user = await self.client.wait_for('reaction_add', timeout=180.0, check=thumb_check)
        except asyncio.TimeoutError:
            logger.info(f'Response not received in time')
            await message.channel.send("Response not confirmed in time; please try again")
        else:
            if str(reaction.emoji) == '👍':
                return True
            elif str(reaction.emoji) == '👎':
                return False
            else:
                return False
