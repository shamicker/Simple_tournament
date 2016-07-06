#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import math
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=simple_tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    delete = "delete from matches;"
    cursor.execute(delete)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    delete = "delete from players;"
    cursor.execute(delete)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = "select count(*) from players;"
    cursor.execute(query)
    result = cursor.fetchall()
    new_result = result[0][0]
    db.close()
    return new_result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cleaned_name = bleach.clean(name)
    query = "insert into players (player_name) values (%s);"
    cursor.execute(query, (cleaned_name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    # query = """
    #     select players.player_id,
    #            players.player_name,
    #            count(a.winner) as wins,
    #            count(b.match_id) as matches
    #     from players
    #         left join matches as a
    #             on players.player_id = a.winner
    #         left join matches as b
    #             on players.player_id in (b.player_1, b.player_2)
    #     group by players.player_id
    #     order by wins desc, players.player_id;
    # """
    # cursor.execute(query)
    # result = cursor.fetchall()
    # #print 'FROM STANDINGS:', result
    cursor.execute("select player_id, player_name, wins, matches from standings;")
    result = cursor.fetchall()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
        
        Args:
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    player_1 = min(winner, loser)
    player_2 = max(winner, loser)
    query = """
        insert into matches
        values (default, %s, %s, %s, %s);
    """
    cursor.execute(query, (player_1, player_2, winner, loser))
    #print (player_1, player_2, winner, loser)
    db.commit()
    db.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
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
    """
    db = connect()
    cursor = db.cursor()
    standings = playerStandings()
    num_players = len(standings)

    total_matches = math.log(num_players) / math.log(2)
    # print "total_matches:", total_matches
    matches_played = standings[0][3]

    # too many rounds?
    if matches_played > total_matches:
        # print "No more total_matches, there's already a winner!"
        return standings

    # round 1 gets random pairing
    elif matches_played == 0:
        random.shuffle(standings)

    # all rounds
    standings_by_id = [row[0:2] for row in standings]
    # print 'STANDINGS BY ID:', standings_by_id
    pairings = []

    i = 0
    while i < num_players:
        pairings.append((standings_by_id[i], standings_by_id[i+1]))
        i += 2

    pairings = [(row[0][0], row[0][1], row[1][0], row[1][1]) for row in pairings]

    print 'PAIRINGS:', pairings
    return pairings

