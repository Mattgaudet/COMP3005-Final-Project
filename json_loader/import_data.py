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
            cursor.execute("""
                INSERT INTO Matches (match_id, match_date, kick_off, competition_id, season_id, home_team_id, 
                home_team_manager_id, away_team_id, away_team_manager_id, home_score, away_score, match_status, 
                match_week, competition_stage_id, stadium_id, referee_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (match['match_id'], match['match_date'], match['kick_off'], match['competition']['competition_id'], 
                match['season']['season_id'], match['home_team']['home_team_id'], match['home_team']['managers'][0]['id'], 
                match['away_team']['away_team_id'], match['away_team']['managers'][0]['id'], match['home_score'], 
                match['away_score'], match['match_status'], match['match_week'], match['competition_stage']['id'],
                match['stadium']['id'], referee_id)
            )
    conn.commit()

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
def insert_into_lineups(conn, lineup_data):
    cursor = conn.cursor()


# Function to parse Match JSON data and insert into tables
def insert_match_data_from_json(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        match_data = json.load(f)
        insert_into_matches(conn, match_data)
        insert_into_teams(conn, match_data)
        insert_into_referees(conn, match_data)
        insert_into_stadiums(conn, match_data)

# Function to parse Competition JSON data and insert into tables
def insert_competition_data_from_jason(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        competition_data = json.load(f)
        insert_into_competitions(conn, competition_data)

# Main function
def main():
    conn = connect_to_database()
    # Matches
    json_file = "json_laoder\\Data\\Matches\\M90.json"  # Path to JSON file La Liga 20/21
    insert_match_data_from_json(conn, json_file)
    json_file = "json_loader\\Data\\Matches\\M44.json"  # Path to JSON file Premier League 03/04
    insert_match_data_from_json(conn, json_file)

    #Competitions
    competition_json_file = "json_loader\\Data\\competitions.json"
    insert_competition_data_from_jason(conn, competition_json_file)
    

    #Lineups
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'Data\\Lineups')
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding="utf-8") as file:
                lineup_data = json.load(file)
                insert_into_lineups(lineup_data)


    conn.close()





if __name__ == "__main__":
    main()
