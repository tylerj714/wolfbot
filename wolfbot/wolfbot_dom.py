#! game.py
# a class for managing game state details
from discord import Guild, User


class Game:
    def __init__(self, game_id: int, creator_discord_id: str, creator_player_id: int, guild_id: int, is_active: bool = False, cur_round_id: int = -1):
        self.game_id = game_id
        self.creator_discord_id = creator_discord_id
        self.creator_player_id = creator_player_id
        self.guild_id = guild_id
        self.is_active = is_active
        self.cur_round_id = cur_round_id
        self.rounds = []
        self.players = []

    @classmethod
    def from_row(cls, row):
        game_id = int(row[0])
        creator_discord_id = str(row[1])
        player_id = int(row[2])
        guild_id = int(row[3])
        is_active = bool(row[4])
        return Game(game_id=game_id,
                    creator_discord_id=creator_discord_id,
                    creator_player_id=player_id,
                    guild_id=guild_id,
                    is_active=is_active
                    )

    def as_string(self):
        return f'game_id:{self.game_id}, ' \
               f'creator_discord_id:{self.creator_discord_id}, ' \
               f'creator_player_id:{self.creator_player_id}, ' \
               f'guild_id:{self.guild_id}, ' \
               f'is_active:{self.is_active}, ' \
               f'cur_round_id:{self.cur_round_id}'


class Player:
    def __init__(self, player_id: int, player_discord_id: str, player_guild_id: str, player_name: str, player_status: str = None, player_replaced_by_id: int = -1):
        self.player_id = player_id
        self.player_discord_id = player_discord_id
        self.player_guild_id = player_guild_id
        self.player_name = player_name
        self.player_status = player_status
        self.player_replaced_by_id = player_replaced_by_id

    @classmethod
    def from_row(cls, row):
        player_id = int(row[0])
        player_discord_id = str(row[1])
        player_guild_id = str(row[2])
        player_name = str(row[3])
        return Player(player_id=player_id,
                      player_discord_id=player_discord_id,
                      player_guild_id=player_guild_id,
                      player_name=player_name)

    def as_string(self):
        return f'player_id:{self.player_id}, ' \
               f'player_discord_id:{self.player_discord_id}, ' \
               f'player_guild_id:{self.player_guild_id}, ' \
               f'player_name:{self.player_name}, ' \
               f'player_status:{self.player_status}'


class Round:
    def __init__(self, round_id, round_tally_mode):
        self.round_id = round_id
        self.round_number = None
        self.round_votes = []
        self.round_start_timestamp = None
        self.round_end_timestamp = None
        self.round_tally_mode = round_tally_mode

    def as_string(self):
        return f'round_id:{self.round_id}, ' \
               f'round_number:{self.round_number}, ' \
               f'round_start_timestamp:{self.round_start_timestamp}, ' \
               f'round_end_timestamp:{self.round_end_timestamp}, ' \
               f'round_tally_mode:{self.round_tally_mode}'


class Vote:
    def __init__(self, vote_id, voter_id, voter_user, voted_id, voted_user, guild):
        self.vote_id = vote_id
        self.player_voting_id = voter_id
        self.vote_player_choice = None
        self.vote_choice = None
        self.vote_timestamp = None

    def as_string(self):
        return f'vote_id:{self.vote_id}, ' \
               f'player_voting_id:{self.player_voting_id}, ' \
               f'vote_player_choice:{self.vote_player_choice}, ' \
               f'vote_choice:{self.vote_choice}, ' \
               f'vote_timestamp:{self.vote_timestamp}'