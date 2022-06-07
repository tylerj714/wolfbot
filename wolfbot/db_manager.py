#! db_manager.py
# a class for managing game state details

import uuid
import sqlite3
from discord import Guild, User
import db_constants
from wolfbot_dom import Game, Player, Round, Vote


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)

    def get_cursor(self):
        return self.connection.cursor()

    def create_game(self, guild: Guild, discord_user: User, player_id: int) -> Game:
        cursor = self.connection.cursor()
        params = (discord_user.id, player_id, guild.id, 1)
        cursor.execute(f"insert into {db_constants.GAME_TABLE} "
                       f"values (null, ?, ?, ?, ?)", params)
        game_id = cursor.lastrowid
        self.connection.commit()
        created_game = Game(game_id=game_id,
                            guild_id=guild.id,
                            creator_player_id=player_id,
                            creator_discord_id=discord_user.id,
                            is_active=True)
        return created_game

    def get_current_game(self, guild: Guild) -> Game:
        cursor = self.connection.cursor()
        cursor.execute(f"select * "
                       f"from {db_constants.GAME_TABLE} "
                       f"where game_guild_id = {guild.id} "
                       f"and game_is_active == 1")
        rows = cursor.fetchall()
        if len(rows) >= 1:
            return Game.from_row(row=rows[0])
        else:
            return None

    def end_game(self, guild: Guild, game_id: int):
        cursor = self.connection.cursor()
        params = (0, guild.id, game_id)
        print(params)
        cursor.execute(f"update {db_constants.GAME_TABLE} "
                       f"set game_is_active = ? "
                       f"where game_guild_id = ? "
                       f"and game_id = ?", params)
        self.connection.commit()

    def get_player(self, guild: Guild, user: User) -> Player:
        cursor = self.connection.cursor()
        cursor.execute(f"select * "
                       f"from {db_constants.PLAYER_TABLE} "
                       f"where player_guild_id = {guild.id} "
                       f"and player_discord_id = {user.id}")
        rows = cursor.fetchall()
        if len(rows) >= 1:
            return Player.from_row(row=rows[0])
        else:
            return None

    def get_player_by_user_id(self, guild: Guild, user_id: str) -> Player:
        cursor = self.connection.cursor()
        cursor.execute(f"select * "
                       f"from {db_constants.PLAYER_TABLE} "
                       f"where player_guild_id = {guild.id} "
                       f"and player_discord_id = {user_id}")
        rows = cursor.fetchall()
        if len(rows) >= 1:
            return Player.from_row(row=rows[0])
        else:
            return None

    def create_player(self, guild: Guild, user: User) -> Player:
        cursor = self.connection.cursor()
        params = (user.id, guild.id, user.display_name)
        cursor.execute(f"insert into {db_constants.PLAYER_TABLE} "
                       f"values (null, ?, ?, ?)", params)
        player_id = cursor.lastrowid
        self.connection.commit()
        created_player = Player(player_id=player_id,
                                player_discord_id=user.id,
                                player_guild_id=guild.id,
                                player_name=user.display_name)
        return created_player
