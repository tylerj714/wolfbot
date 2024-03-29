#! db_constants.py
# a class for defining constants used in tables

#DB Related Constants
WOLFBOT_DB = "wolfbot.db"
GAME_TABLE = "game"
ROUND_TABLE = "round"
PLAYER_TABLE = "player"
VOTE_TABLE = "vote"
GAME_PLAYER_TABLE = "game_player"
GAME_ROUND_TABLE = "game_round"

#Player Status
PLAYER_ALIVE = "alive"
PLAYER_REPLACED = "replaced"
PLAYER_DEAD = "dead"
PLAYER_REMOVED = "removed"

#Vote For Method
VOTE_METHOD_PLAYER = "vm_player"
VOTE_METHOD_LIST = "vm_pdfl"

#Vote Placeholders
VOTE_NOBODY = "nobody"
VOTE_UNVOTE = "unvote"

#Vote Calculation Algorithm Types
VOTE_CALC_MAJORITY = "maj"
VOTE_CALC_PLURALITY = "plur"
VOTE_CALC_RANKED_CHOICE = "rcv"