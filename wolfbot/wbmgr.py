# wbmgr.py
# manages responding to message requests
from typing import List

from wolfbot_dom import *
from discord import Reaction, User, Guild, Client, Message, Member, TextChannel, app_commands, Interaction, Role
from discord.app_commands.commands import Command
from discord.app_commands import Namespace
from discord.utils import get
from db_manager import DBManager
import db_constants
import asyncio
from logging_manager import logger
import time
import re
from typing import List, Optional, Literal

mod_roles = ['moderator', 'administrator']

class WBManager:
    def __init__(self, client):
        self.client = client

    async def help(self):

        return

    async def getMember(self, user_id: str) -> Member:
        member = get(self.client.get_all_members(), id=user_id)
        return member

    async def has_moderator_role(self, interaction: Interaction) -> bool:
        user_roles: List[str] = [role.name.lower() for role in interaction.user.roles]
        if not any(role in mod_roles for role in user_roles):
            logger.info(f"No moderator role found within {user_roles} for user {interaction.user.id}->{interaction.user.name}")
            return False
        else:
            logger.info(f"Moderator role found within {user_roles} for user {interaction.user.id}->{interaction.user.name}")
            return True

    async def game_manage(self, interaction: Interaction, action: str) -> str:
        if not await self.has_moderator_role(interaction):
            return "Managing game settings requires Moderator or Administrator role!"

        dbmgr = DBManager()
        current_game = dbmgr.get_current_game(interaction.guild)
        response_message = ""

        if action == 'Create':
            if current_game is None:
                new_game = dbmgr.create_game(interaction.guild, interaction.user, interaction.user.id)
                response_message = f"Created new game #{new_game.game_id} for server id {new_game.guild_id}"
            else:
                response_message = "Error! There is already an active game on this server!"
        elif action == 'End':
            if current_game is None:
                response_message = "Error! There is currently no active game on this server!"
            else:
                dbmgr.end_game(interaction.guild, current_game.game_id)
                response_message = f"Ended game #{current_game.game_id} for server id {current_game.guild_id}"

        dbmgr.connection.close()
        return response_message

    async def game_player(self, interaction: Interaction, action: str, member: Member, replacement: Optional[Member]):
        if not await self.has_moderator_role(interaction):
            return "Managing game settings requires Moderator or Administrator role!"

        dbmgr = DBManager()
        current_game = dbmgr.get_current_game(interaction.guild)
        response_message = ""

        if current_game is None:
            return "Error! There is currently no active game on this server!"

        if action == 'Add':
            #Check to make sure player doesn't already exist
            current_player = dbmgr.get_player(interaction.guild, member)
            if current_player is not None:
                response_message = f"Player {current_player.player_name} already exists!"
            else:
                new_player = dbmgr.create_player(interaction.guild, interaction.user)
                response_message = f"Added player {new_player.player_name} to game #{current_game}"
        elif action == 'Remove':
            #Check to make sure player is registered to this game
            current_player = dbmgr.get_player(interaction.guild, member)
            if current_player is not None:
                updated_player = dbmgr.update_player_status(db_constants.PLAYER_REMOVED, current_game, current_player)
                response_message = f"Player {updated_player.player_name} status has been updated to {updated_player.player_status}"
            else:
                response_message = f"No player for member {member.id}->{member.name}"
        elif action == 'Kill':
            #Check to make sure player is registered to this game
            current_player = dbmgr.get_player(interaction.guild, member)
            if current_player is not None:
                updated_player = dbmgr.update_player_status(db_constants.PLAYER_DEAD, current_game, current_player)
                response_message = f"Player {updated_player.player_name} status has been updated to {updated_player.player_status}"
            else:
                response_message = f"No player for member {member.id}->{member.name}"
        elif action == 'Revive':
            #Check to make sure player is registered to this game
            current_player = dbmgr.get_player(interaction.guild, member)
            if current_player is not None:
                updated_player = dbmgr.update_player_status(db_constants.PLAYER_ALIVE, current_game, current_player)
                response_message = f"Player {updated_player.player_name} status has been updated to {updated_player.player_status}"
            else:
                response_message = f"No player for member {member.id}->{member.name}"
        elif action == 'Replace':
            #Check to make sure player is registered to this game
            current_player = dbmgr.get_player(interaction.guild, member)
            if replacement is None:
                response_message = f"withplayer argument is required when doing a replacement"
                dbmgr.connection.close()
                return response_message

            replacement_player = dbmgr.get_player(interaction.guild, replacement)
            if current_player is not None and replacement_player is not None:
                dbmgr.replace_player(current_game, current_player)
                updated_player = dbmgr.update_player_status(db_constants.PLAYER_ALIVE, current_game, current_player)
                response_message = f"Player {updated_player.player_name} status has been updated to {updated_player.player_status}"
            else:
                if current_player is None:
                    response_message = f"No player for member {member.id}->{member.name} found; make sure they've been added to the game first"
                elif replacement_player is None:
                    response_message = f"No player for member {replacement.id}->{replacement.name} found; make sure they've been added to the game first"

        dbmgr.connection.close()
        return response_message
