#! game.py
# a class for managing game state details

import uuid


class Round:
    def __init__(self, user, guild):
        self.round_id = None
        self.round_number = None
        self.round_votes = []
        self.round_start_timestamp = None
        self.round_end_timestamp = None
        self.round_tally_mode = None
