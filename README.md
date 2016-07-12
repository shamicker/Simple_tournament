# Simple_tournament
Udacity IPND/Fullstack Tournament Project

This is my basic version of the Project. It was created so I could figure out what I was doing, and then to build on that for the more complicated, multi-tournament one.

- I can't figure out how to merge all the tournament projects (the original fork, the simple version, and the multi-tournament version) into one. When I figure it out, I'll merge them together.

# Tournament Planner

Keep track of players and game matches in a tournament!  Uses the Swiss-style, non-elimination method to pair up rivals with similar standings.

## Files and Set Up

This Python module uses the PostgreSQL database. (I don't know how others would do it because I don't really understand it, but I'm logged into Vagrant.)

The **simple_tournament.sql** file has the database schema. From the PostgreSQL command line, type `\i simple_tournament.sql` to import the file into psql.
This will:
- drop any previous database called 'simple_tournament'
- create a new one
- connect you to it
- set up the tables and views

The **simple_tournament.py** file stores the Python code for adding, viewing, and fetching data.

The **simple_tournament_test.py** file is the sample test from the course to help the student along. It runs the **simple_tournament.py** file and lets you (the student) know what tests are passing and where you're failing. Run this from the command line, using the command `python simple_tournament_test.py`.

## The Database

**`players`**
This table lists players in a game.
  - `person_id` - the unique id of an available person
  - `person_name` - the person's name; can be a duplicate.
  - `date_created` - automatic date and time of creation

**`matches`**
This table lists matches played and the outcomes. There are no tied games.
  - `match_id` - the unique id of a single match
  - `player_1` - one of the players by `person_id`
  - `player_2` - the rival
  - `winner` - the `person_id` of the winner of the match
  - `loser` - the `person_id` of the loser of the match


**`standings`**
This table lets you view of the standing per game.
  - `player_id` - the unique id of a player
  - `player_name` - the player's name
  - `wins` - the number of wins per player
  - `matches` - the number of matches per player
  - 

## Functions in tournament.py

**connect()**
Connects to the PostgreSQL database. Returns a database connection. 
Was part of the template.


**deleteMatches(`game=None`)**
Removes all the match records from the database.


**deletePlayers(`player_id=None`)**
Removes all the player records from the database.


**countPlayers()**
Returns the number of players currently registered.


**registerPlayer(`name, person_id=None, game=None`)**
Adds a player to the tournament database. 

The database assigns a unique serial id number for the player.

Args:
  name: the player's full name (need not be unique).


**playerStandings(`game=None`)**
Returns a list of the players and their win records, sorted by wins.

The first entry in the list should be the player in first place, or a player
tied for first place if there is currently a tie.

Returns:
  A list of tuples, each of which contains (id, name, wins, matches):
    id: the player's unique id (assigned by the database)
    name: the player's full name (as registered)
    wins: the number of matches the player has won
    matches: the number of matches the player has played


**reportMatch(`game, player, player_status=None, opponent=None`)**
Records the outcome of a single match between two players.

Args:
winner:  the id number of the player who won
loser:  the id number of the player who lost


**swissPairings(`game=None`)**
Returns a list of pairs of players for the next round of a match.

Assuming that there are an even number of players registered, each player
appears exactly once in the pairings.  Each player is paired with another
player with an equal or nearly-equal win record, that is, a player adjacent
to him or her in the standings.

Returns:
  A list of tuples, each of which contains (id1, name1, id2, name2)
    id1: the first player's unique id
    name1: the first player's name
    id2: the second player's unique id
    name2: the second player's name
