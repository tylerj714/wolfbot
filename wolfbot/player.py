#! game.py
# a class for managing game state details

import uuid


class Player:
    def __init__(self, user, guild):
        self.id = user
        self.player_name = user
        self.player_status = None
