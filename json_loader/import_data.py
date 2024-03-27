import json
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

# Function to parse JSON data and insert into tables
def insert_match_data_from_json(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        match_data = json.load(f)
        insert_into_matches(conn, match_data)
        insert_into_teams(conn, match_data)
        insert_into_referees(conn, match_data)
        insert_into_stadiums(conn, match_data)

# Main function
def main():
    conn = connect_to_database()
    json_file = "Data\Matches\A1.json"  # Path to JSON file
    insert_match_data_from_json(conn, json_file)
    conn.close()

if __name__ == "__main__":
    main()
