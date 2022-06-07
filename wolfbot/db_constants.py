#! db_constants.py
# a class for defining constants used in tables

#DB Related Constants
WOLFBOT_DB = "wolfbot.db"
GAME_TABLE = "game"
ROUND_TABLE = "round"
PLAYER_TABLE = "player"
VOTE_TABLE = "vote"

#Vote For Method
VOTE_METHOD_PLAYER = "vm_player"
VOTE_METHOD_LIST = "vm_pdfl"

#Vote Calculation Algorithm Types
VOTE_CALC_MAJORITY = "maj"
VOTE_CALC_PLURALITY = "plur"
VOTE_CALC_RANKED_CHOICE = "rcv"