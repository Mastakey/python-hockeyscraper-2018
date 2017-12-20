create table games (
    id INTEGER primary key AUTOINCREMENT,
    gamedate varchar(80),
    hteam varchar(80),
    vteam varchar(80),
    link varchar(1000),
    season varchar(10),
    isparsed varchar(5)
);

create table boxscore_player_data (
    id INTEGER primary key AUTOINCREMENT,
    game INTEGER,
    team varchar(80),
    oppteam varchar(80),
    player varchar(255),
    goals INTEGER,
    assists INTEGER,
    goals_ev INTEGER,
    goals_pp INTEGER,
    goals_sh INTEGER,
    goals_gw INTEGER,
    assists_ev INTEGER,
    assists_pp INTEGER,
    assists_sh INTEGER,
    shots INTEGER,
    time_on_ice varchar(10),
    time_on_ice_s INTEGER
);

create table boxscore_goalie_data (
    id INTEGER primary key AUTOINCREMENT,
    game INTEGER,
    team varchar(80),
    oppteam varchar(80),
    player varchar(255),
    decision INTEGER,
    goals_against INTEGER,
    shots_against INTEGER,
    saves INTEGER,
    save_pct REAL,
    shutouts INTEGER,
    time_on_ice varchar(10),
    time_on_ice_s INTEGER
);