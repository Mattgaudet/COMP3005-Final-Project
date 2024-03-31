import json
import os
import psycopg
from psycopg import Error

# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    return conn

# Function to insert data into the Matches table
def insert_into_matches(conn, match_data):
    cursor = conn.cursor()
    for match in match_data:
        # Check if the team already exists in the table
        cursor.execute("SELECT 1 FROM Matches WHERE match_id = %s", (match['match_id'],))
        existing_match = cursor.fetchone()
        if not existing_match:
            if match.get('referee') is not None: #since referee is sometimes None
                referee_id = match['referee']['id']
            else:
                referee_id = None
            if match.get('stadium') is not None:
                stadium_id = match['stadium']['id']
            else:
                stadium_id = None
            cursor.execute("""
                INSERT INTO Matches (match_id, match_date, kick_off, competition_id, season_id, home_team_id, 
                away_team_id, home_score, away_score, match_status, 
                match_week, competition_stage_id, stadium_id, referee_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (match['match_id'], match['match_date'], match['kick_off'], match['competition']['competition_id'], 
                match['season']['season_id'], match['home_team']['home_team_id'], match['away_team']['away_team_id'], 
                match['home_score'], match['away_score'], match['match_status'], match['match_week'], 
                match['competition_stage']['id'], stadium_id, referee_id)
            )
    conn.commit()

def insert_into_managers(conn, match_data):
    cursor = conn.cursor()
    for match in match_data:
        insert_into_managers_helper(cursor, match, match['home_team'])
        insert_into_managers_helper(cursor, match, match['away_team'])
    conn.commit()
        

def insert_into_managers_helper(cursor, match, team):
    if team.get('managers') is not None:
        managers = team['managers']
        for manager in managers:
            # Check if the team already exists in the table
            cursor.execute("SELECT 1 FROM Managers WHERE manager_id = %s", (manager['id'],))
            existing_manager = cursor.fetchone()
            if not existing_manager:
                cursor.execute("""
                    INSERT INTO Managers (manager_id, name, nickname, dob, country_id)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (manager['id'], manager['name'], manager['nickname'],
                    manager['dob'], manager['country']['id'])
                )
            cursor.execute("""
                INSERT INTO Match_Managers (match_id, manager_id)
                VALUES (%s, %s)""",
                (match['match_id'], manager['id'])
            )

# Function to insert data into the Teams table
def insert_into_teams(conn, match_data):
    cursor = conn.cursor()

    for match in match_data:
        home_team = match['home_team']
        away_team = match['away_team']
        # Check if the team already exists in the table
        cursor.execute("SELECT 1 FROM Teams WHERE team_id = %s", (home_team['home_team_id'],))
        existing_home_team = cursor.fetchone()
        cursor.execute("SELECT 1 FROM Teams WHERE team_id = %s", (away_team['away_team_id'],))
        existing_away_team = cursor.fetchone()
        
        # Insert home team
        if not existing_home_team:
            cursor.execute("""
                INSERT INTO Teams (team_id, team_name, team_gender, team_group, country_id)
                VALUES (%s, %s, %s, %s, %s)""",
                (home_team['home_team_id'], home_team['home_team_name'], home_team['home_team_gender'],
                home_team['home_team_group'], home_team['country']['id'])
            )
            
        # Insert away team
        if not existing_away_team:
            cursor.execute("""
                INSERT INTO Teams (team_id, team_name, team_gender, team_group, country_id)
                VALUES (%s, %s, %s, %s, %s)""",
                (away_team['away_team_id'], away_team['away_team_name'], away_team['away_team_gender'],
                away_team['away_team_group'], away_team['country']['id'])
                )
        conn.commit()


# Function to insert data into the Referees table
def insert_into_referees(conn, match_data):
    cursor = conn.cursor()
    for match in match_data:
        if 'referee' in match:
            referee = match['referee']
            
            # Check if the referee already exists in the table
            cursor.execute("SELECT 1 FROM Referees WHERE referee_id = %s", (referee['id'],))
            existing_referee = cursor.fetchone()
            if not existing_referee:
                cursor.execute("""
                    INSERT INTO Referees (referee_id, name, country_id)
                    VALUES (%s, %s, %s)""",
                    (referee['id'], referee['name'], referee['country']['id'])
                )
    conn.commit()

# Function to insert data into the Stadiums table
def insert_into_stadiums(conn, match_data):
    cursor = conn.cursor()
    for match in match_data:
        if match.get('stadium') is not None:
            stadium = match['stadium']
            # Check if the team already exists in the table
            cursor.execute("SELECT 1 FROM Stadiums WHERE stadium_id = %s", (stadium['id'],))
            existing_stadium = cursor.fetchone()
            if not existing_stadium:
                cursor.execute("""
                    INSERT INTO Stadiums (stadium_id, stadium_name, country_id)
                    VALUES (%s, %s, %s)""",
                    (stadium['id'], stadium['name'], stadium['country']['id'])
                )
    conn.commit()

# Function to insert data into the Stadiums table
def insert_into_competitions(conn, competition_data):
    cursor = conn.cursor()
    for comp in competition_data:
        # Check if the team already exists in the table
        cursor.execute("SELECT 1 FROM Competitions WHERE competition_id = %s", (comp['competition_id'],))
        existing_competition = cursor.fetchone()
        if not existing_competition:
            cursor.execute("""
                INSERT INTO Competitions (competition_id, season_id, country_name, competition_name, competition_gender,
                competition_youth, competition_international, season_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (comp['competition_id'], comp['season_id'], comp['country_name'], comp['competition_name'], 
                 comp['competition_gender'], comp['competition_youth'], comp['competition_international'], comp['season_name'])
            )
    conn.commit()

# Function to insert data into the Lineups table
def insert_into_lineups(conn, lineup_data, match):
    cursor = conn.cursor()
    for lineup in lineup_data:
        lineup_obj = lineup['lineup']
        for item in lineup_obj:
            cursor.execute("""
                INSERT INTO Lineups (match_id, team_id, team_name, player_id, player_name, player_nickname, 
                jersey_number, country_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (match, lineup['team_id'], lineup['team_name'], item['player_id'], item['player_name'], 
                    item['player_nickname'], item['jersey_number'], item['country']['id'])
            )
    conn.commit()

# Function to insert data into the cards table
def insert_into_cards(conn, lineup_data, match):
    cursor = conn.cursor()
    for lineup in lineup_data:
        lineup_obj = lineup['lineup']
        for item in lineup_obj:
            cards = item['cards']
            for card in cards:
                cursor.execute("""
                    INSERT INTO Cards (match_id, player_id, time, card_type, reason, period)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (match, item['player_id'], card['time'], card['card_type'], card['reason'], card['period'])
                )
    conn.commit()

# Function to insert data into the positions table
def insert_into_positions(conn, lineup_data, match):
    cursor = conn.cursor()
    for lineup in lineup_data:
        lineup_obj = lineup['lineup']
        for item in lineup_obj:
            positions = item['positions']
            for position in positions:
                cursor.execute("""
                    INSERT INTO Positions (match_id, player_id, position, from_time, to_time, from_period, 
                    to_period, start_reason, end_reason)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (match, item['player_id'], position['position'], position['from'], position['to'], 
                     position['from_period'], position['to_period'], position['start_reason'], position['end_reason'])
                )
    conn.commit()


# Function to parse Match JSON data and insert into tables
def insert_match_data_from_json(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        match_data = json.load(f)
        insert_into_matches(conn, match_data)
        insert_into_managers(conn, match_data)
        insert_into_teams(conn, match_data)
        insert_into_referees(conn, match_data)
        insert_into_stadiums(conn, match_data)

# Function to parse Competition JSON data and insert into tables
def insert_competition_data_from_json(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        competition_data = json.load(f)
        insert_into_competitions(conn, competition_data)

# Function to parse Competition JSON data and insert into tables
def insert_lineup_data_from_json(conn, json_file, filename):
    with open(json_file, 'r', encoding="utf-8") as file:
        lineup_data = json.load(file)
        match_id = filename[:7]
        insert_into_lineups(conn, lineup_data, match_id)
        insert_into_cards(conn, lineup_data, match_id)
        insert_into_positions(conn, lineup_data, match_id)


# Main function
def main():
    conn = connect_to_database()
    # Matches
    json_file = "json_loader\\Data\\Matches\\M90.json"  # Path to JSON file La Liga 20/21
    insert_match_data_from_json(conn, json_file)
    json_file = "json_loader\\Data\\Matches\\M44.json"  # Path to JSON file Premier League 03/04
    insert_match_data_from_json(conn, json_file)

    #Competitions
    competition_json_file = "json_loader\\Data\\competitions.json"
    insert_competition_data_from_json(conn, competition_json_file)
    
    #Lineups (add all files from the Lineups folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'Data\\Lineups')
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_path = os.path.join(folder_path, filename)
            insert_lineup_data_from_json(conn, file_path, filename)
            
    #Events (add all files from the Events folder)





    conn.close()


if __name__ == "__main__":
    main()
