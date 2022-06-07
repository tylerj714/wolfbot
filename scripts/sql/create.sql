CREATE TABLE game (
    game_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    game_owner_discord_id   TEXT NOT NULL,
    game_owner_player_id    INTEGER,
    game_guild_id           TEXT    NOT NULL,
    game_is_active          INTEGER NOT NULL
);

CREATE TABLE round (
    round_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    round_number          INTEGER NOT NULL,
    round_tally_mode      TEXT    NOT NULL,
    round_start_timestamp TEXT    NOT NULL,
    round_end_timestamp   TEXT    NOT NULL
);

CREATE TABLE player (
    player_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    player_discord_id   TEXT    NOT NULL,
    player_guild_id     TEXT    NOT NULL,
    player_name         TEXT    NOT NULL
);

CREATE TABLE vote (
    vote_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    player_voting     TEXT    NOT NULL,
    player_voted      TEXT    NOT NULL,
    vote_timestamp    TEXT    NOT NULL
);

CREATE TABLE game_round (
    game_id   INTEGER NOT NULL,
    round_id  INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (round_id) REFERENCES round(round_id)
);

CREATE TABLE game_player (
    game_id     INTEGER NOT NULL,
    player_id   INTEGER NOT NULL,
    player_game_status  TEXT NOT NULL,
    player_replaced_by_id   INTEGER,
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

CREATE TABLE round_vote (
    vote_id     INTEGER NOT NULL,
    round_id    INTEGER NOT NULL,
    FOREIGN KEY (vote_id) REFERENCES vote(vote_id),
    FOREIGN KEY (round_id) REFERENCES round(round_id)
);

CREATE TABLE player_vote (
    player_id   INTEGER NOT NULL,
    vote_id     INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (vote_id) REFERENCES vote(vote_id)
);