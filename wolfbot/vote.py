#! game.py
# a class for managing game state details

import uuid


class Vote:
    def __init__(self, user, guild):
        self.vote_id = None
        self.player_voting = user
        self.player_voted = None
        self.vote_timestamp = None