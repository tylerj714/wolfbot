# wbmain.py
import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from typing import List, Optional, Literal
from logging_manager import logger
from wbmgr import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BASE_PATH = os.getenv('BASE_PATH')

class WBClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 947928220093788180))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = WBClient()
tree = app_commands.CommandTree(client)
wb_mgr = WBManager(client)

@tree.command(name = "game-manage", description = "Used for starting an ending a game on a discord server.", guild = discord.Object(id = 947928220093788180))
async def game_manage(interaction: discord.Interaction, action: Literal['Create', 'End']):
    await interaction.response.send_message(f"You chose {action}")

@tree.command(name="game-player", description="Used for adding, removing, replacing, or changing status of a player", guild=discord.Object(id = 947928220093788180))
@app_commands.describe(
    action="The operation you wish to perform for this player",
    player="The player you wish to perform the action for",
    withplayer="Only for use with 'Replace' action; a player to replace chosen player in the 'player' argument"
)
async def game_player(interaction: discord.Interaction, action: Literal['Add', 'Remove', 'Kill', 'Replace'], player: discord.Member, withplayer: Optional[discord.Member] = None):
    with_player = withplayer.name if withplayer is not None else "nobody"
    await interaction.response.send_message(f'You chose {action} and {player} and {with_player}')

@tree.command(name="round-create", description="Used for creating a voting round", guild=discord.Object(id = 947928220093788180))
@app_commands.describe(
    votetype="The voting style for this round: Player or Choice; default is Player",
    votetabulate="How the vote should be tabulated: Plurality or Majority; default is Plurality",
    lockonmajority="When Majority is selected, determine if the vote should lock once majority is reached; default is no",
    hiddenvote="Determines if vote-tally usage will hide voter names; default is no",
    roundstart="Epoch timestamp for when votes will be allowed to be cast; if no timestamp is provided, voting opens immediately",
    roundend="Epoch timestamp for when votes will no longer be accepted; if no timestamp is provided, voting is open until manually closed",
    reportchannel="Channel name or ID for voting results to be displayed in; if not set, vote results will be returned in the channel the bot was called"

)
async def round_create(
        interaction: discord.Interaction,
        votetype: Optional[Literal['Player', 'Choice']] = 'Player',
        votetabulate: Optional[Literal['Plurality', 'Majority']] = 'Plurality',
        lockonmajority: Optional[Literal['yes', 'no']] = 'no',
        hiddenvote: Optional[Literal['yes', 'no']] = 'no',
        roundstart: Optional[int] = None,
        roundend: Optional[int] = None,
        reportchannel: Optional[str] = None
):
    round_start_time = roundstart if roundstart is not None else -1
    round_end_time = roundend if roundend is not None else -1
    report_channel = reportchannel if reportchannel is not None else interaction.channel

    await interaction.response.send_message(f'You chose {votetype}, {votetabulate}, {lockonmajority}, {hiddenvote}, {roundend}, and {reportchannel}')

@tree.command(name='round-manage', description="Used for managing the round parameters or to end the round", guild=discord.Object(id = 947928220093788180))
async def round_manage(
        interaction: discord.Interaction,
        action: Literal['Alter', 'End'],
        parameter: Optional[Literal['lockonmajority', 'roundstart', 'roundend', 'reportchannel']] = None,
        value: Optional[str] = None
):
    await interaction.response.send_message(f'You chose {action}')

@tree.command(name='vote-tally', description="Used to get the latest vote tally. By default gets the tally of the currently active round.", guild=discord.Object(id = 947928220093788180))
async def vote_tally(interaction: discord.Interaction, round: Optional[int] = None):
    await interaction.response.send_message(f'The vote results for round are: TBD')

@tree.command(name='vote-history', description="Used to get the vote history. By default gets the currently active round.", guild=discord.Object(id = 947928220093788180))
async def vote_history(interaction: discord.Interaction, round: Optional[int] = None):
    await interaction.response.send_message(f'This is just a placeholder for now')

@tree.command(name='vote-player', description="Allows voting for a player, clearing your vote, or selecting no vote.", guild=discord.Object(id = 947928220093788180))
@app_commands.describe(
    player="The player you are voting for.",
    other="Select 'No Vote' to select nobody.\n Select 'Unvote' to clear your current vote."
)
async def vote_player(interaction: discord.Interaction, player: Optional[discord.Member] = None, other: Optional[Literal['No Vote', 'Unvote']] = None):
    player_choice = player if player is not None else "nobody"
    other_choice = other if other is not None else "none"
    await interaction.response.send_message(f'You chose {player_choice} and {other_choice}')

@tree.command(name='vote-choice', description="Allows voting for a choice by entering a number. An entry of 0 will clear an existing vote.", guild=discord.Object(id = 947928220093788180))
async def vote_choice(interaction: discord.Interaction, choice: app_commands.Range[int, 0, 9] = 0):
    await interaction.response.send_message(f'You selected option #{choice}')

client.run(TOKEN)
