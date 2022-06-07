import unittest
from wolfbot.db_manager import DBManager
from wolfbot import db_constants
from discord import Guild, User


class TestDBManager(unittest.TestCase):

    def test_game_insert(self):
        dbmgr = DBManager(db_constants.WOLFBOT_DB)


if __name__ == '__main__':
    unittest.main()
