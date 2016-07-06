-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- delete and drop anything that might previously exist
drop database if exists simple_tournament;

-- create database named tournament
create database simple_tournament;

-- connect to tournament database
\c simple_tournament


create table players (
	player_id serial primary key,
	player_name varchar not null,
	datecreated timestamp default current_timestamp,
	unique (player_id, player_name)
	);


create table matches (
	match_id serial primary key,
	player_1 serial references players,
	player_2 serial references players (player_id),
	winner serial references players (player_id),
	loser serial references players (player_id),
	check (player_1 < player_2),
	check (winner != loser),
	unique (player_1, player_2)
	);


create view standings as
	select players.player_id,
           players.player_name,
           count(a.winner) as wins,
           count(b.match_id) as matches
    from players 
        left join matches as a 
            on players.player_id = a.winner
        left join matches as b 
            on players.player_id in (b.player_1, b.player_2)
    group by players.player_id
    order by wins desc, players.player_id;


select * from players;
select * from matches;
select * from standings;
