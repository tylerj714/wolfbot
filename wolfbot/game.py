#! game.py
# a class for managing game state details

import uuid


class Game:
    def __init__(self, user, guild):
        self.id = uuid.uuid4().hex
        self.creator = user
        self.guild = guild
        self.cur_round = None
        self.rounds = []
        self.players = []
