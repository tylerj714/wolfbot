#! db_manager.py
# a class for managing game state details

import uuid
import typing
import sqlite3
from discord import Guild, User
import db_constants
from wolfbot_dom import Game, Player, Round, Vote
from logging_manager import logger


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)

    def get_cursor(self):
        return self.connection.cursor()

    def create_game(self, guild: Guild, discord_user: User, player_id: int) -> Game:
        cursor = self.connection.cursor()
        params = (discord_user.id, player_id, guild.id, 1)
        sql = f'insert into {db_constants.GAME_TABLE} ' \
              f'values (null, ?, ?, ?, ?)'
        logger.info(f'inserting into game: {sql}; {params}')
        cursor.execute(sql, params)
        game_id = cursor.lastrowid
        self.connection.commit()
        game = Game(game_id=game_id,
                    guild_id=guild.id,
                    creator_player_id=player_id,
                    creator_discord_id=discord_user.id,
                    is_active=True)
        logger.info(f'created game: {Game.as_string(game)}')
        return game

    def get_current_game(self, guild: Guild) -> Game:
        cursor = self.connection.cursor()
        sql = f"select * " \
              f"from {db_constants.GAME_TABLE} " \
              f"where game_guild_id = {guild.id} " \
              f"and game_is_active == 1"
        logger.info(f'Running query: {sql}')
        cursor.execute(sql)
        record = cursor.fetchone()
        if record is not None:
            game = Game.from_row(row=record)
            logger.info(f'retrieved game: {Game.as_string(game)}')
            return game
        else:
            logger.info(f'no active game found for guild {guild.name}')
            return None

    def end_game(self, guild: Guild, game_id: int):
        cursor = self.connection.cursor()
        params = (0, guild.id, game_id)
        sql = f"update {db_constants.GAME_TABLE} " \
              f"set game_is_active = ? " \
              f"where game_guild_id = ? " \
              f"and game_id = ?"
        logger.info(f'updating game: {sql}; {params}')
        cursor.execute(sql, params)
        self.connection.commit()

    def get_player(self, guild: Guild, user: User) -> Player:
        cursor = self.connection.cursor()
        sql = f'select * ' \
              f'from {db_constants.PLAYER_TABLE} ' \
              f'where player_guild_id = {guild.id} ' \
              f'and player_discord_id = {user.id}'
        logger.info(f'Running query: {sql}')
        cursor.execute(sql)
        record = cursor.fetchone()
        if record is not None:
            player = Player.from_row(row=record)
            logger.info(f'retrieved player: {Player.as_string(player)}')
            return player
        else:
            logger.info(f'no player found')
            return None

    def get_player_by_user_id(self, guild: Guild, user_id: str) -> Player:
        cursor = self.connection.cursor()
        sql = f'select * ' \
              f'from {db_constants.PLAYER_TABLE} ' \
              f'where player_guild_id = {guild.id} ' \
              f'and player_discord_id = {user_id}'
        logger.info(f'Running query: {sql}')
        cursor.execute(sql)
        record = cursor.fetchone()
        if record is not None:
            player = Player.from_row(row=record)
            logger.info(f'retrieve player: {Player.as_string(player)}')
            return Player.from_row(row=record)
        else:
            logger.info(f'no player found')
            return None

    def get_players_in_game(self, guild: Guild, game: Game) -> typing.List[Player]:
        cursor = self.connection.cursor()
        sql = f'select p.*, gp.player_game_status, gp.player_replaced_by_id ' \
              f'from {db_constants.GAME_TABLE} g ' \
              f'join {db_constants.GAME_PLAYER_TABLE} gp ' \
              f'on g.game_id = gp.game_id ' \
              f'join {db_constants.PLAYER_TABLE} p ' \
              f'on gp.player_id = p.player_id ' \
              f'where g.game_guild_id = {guild.id} ' \
              f'and g.game_id = {game.game_id}'
        logger.info(f'Running query: {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        player_list = []
        for row in rows:
            player = Player(player_id=int(row[0]),
                            player_discord_id=str(row[1]),
                            player_guild_id=str(row[2]),
                            player_name=str(row[3]),
                            player_status=str(row[4]),
                            player_replaced_by_id=int(row[5]) if row[5] is not None else -1)
            logger.info(f'retrieved player: {Player.as_string(player)}')
            player_list.append(player)
        return player_list

    def create_player(self, guild: Guild, user: User) -> Player:
        cursor = self.connection.cursor()
        params = (user.id, guild.id, user.display_name)
        sql = f'insert into {db_constants.PLAYER_TABLE} ' \
              f'values (null, ?, ?, ?)'
        logger.info(f'insert into player: {sql}; {params}')
        cursor.execute(sql, params)
        player_id = cursor.lastrowid
        self.connection.commit()
        player = Player(player_id=player_id,
                        player_discord_id=user.id,
                        player_guild_id=guild.id,
                        player_name=user.display_name)
        logger.info(f'created player: {Player.as_string(player)}')
        return player

    def update_player_name(self, player_id: int, guild: Guild, user: User) -> Player:
        cursor = self.connection.cursor()
        params = (user.display_name, player_id, guild.id, user.id)
        sql = f'update {db_constants.PLAYER_TABLE} ' \
              f'set player_name = ? ' \
              f'where player_id = ? ' \
              f'and player_guild_id = ? ' \
              f'and player_discord_id = ?'
        logger.info(f'updating player: {sql}; {params}')
        cursor.execute(sql, params)
        self.connection.commit()
        player = Player(player_id=player_id,
                        player_discord_id=user.id,
                        player_guild_id=guild.id,
                        player_name=user.display_name)
        logger.info(f'updated player: {Player.as_string(player)}')
        return player

    def get_game_player(self, game: Game, player: Player):
        cursor = self.connection.cursor()
        params = (game.game_id, player.player_id)
        sql = f'select * ' \
              f'from {db_constants.GAME_PLAYER_TABLE} ' \
              f'where game_id = ? ' \
              f'and player_id = ?'
        logger.info(f'running query {sql}; {params}')
        cursor.execute(sql, params)
        record = cursor.fetchone()
        if record is not None:
            player.player_status = str(record[2])
            game.players.append(player)
            logger.info(f'retrieved player {player.as_string}')
            return Player
        else:
            logger.info(f'no player found')
            return None

    def add_player_to_game(self, game: Game, player: Player):
        cursor = self.connection.cursor()
        params = (game.game_id, player.player_id, db_constants.PLAYER_ALIVE)
        sql = f'insert into {db_constants.GAME_PLAYER_TABLE} ' \
              f'values (?, ?, ?, null)'
        logger.info(f'inserting into game_player: {sql}; {params}')
        cursor.execute(f"insert into {db_constants.GAME_PLAYER_TABLE} "
                       f"values (?, ?, ?, null)", params)
        self.connection.commit()
        return

    def replace_player(self, game: Game, player_to_replace: Player, player_replacing: Player):
        cursor = self.connection.cursor()
        params = (db_constants.PLAYER_REPLACED, player_replacing.player_id, game.game_id, player_to_replace.player_id)
        sql = f'update {db_constants.GAME_PLAYER_TABLE} ' \
              f'set player_game_status = ?, player_replaced_by_id = ? ' \
              f'where game_id = ? ' \
              f'and player_id = ?'
        logger.info(f'updating player: {sql}; {params}')
        cursor.execute(sql, params)
        self.connection.commit()
        return

    def update_player_status(self, status: str, game: Game, player: Player) -> Player:
        cursor = self.connection.cursor()
        params = (status, game.game_id, player.player_id)
        sql = f'update {db_constants.GAME_PLAYER_TABLE} ' \
              f'set player_game_status = ? ' \
              f'where game_id = ? ' \
              f'and player_id = ?'
        logger.info(f'updating player: {sql}; {params}')
        cursor.execute(sql, params)
        self.connection.commit()
        player.player_status = status
        logger.info(f'updated player: {Player.as_string(player)}')
        return player
