import psycopg
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = 5432

try:
    #connect to the database
    conn = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    #create a cursor
    cursor = conn.cursor()

    #create the competitions table 
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Competitions (
            competition_id INT PRIMARY KEY UNIQUE,
            season_id INT,
            country_name VARCHAR(30),
            competition_name VARCHAR(30),
            competition_gender VARCHAR(20),
            competition_youth BOOLEAN,
            competition_international BOOLEAN,
            season_name VARCHAR(20)
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("competitions database table created")

    #create the matches table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Matches (
            match_id INT PRIMARY KEY,
            match_date DATE,
            kick_off VARCHAR(20),
            competition_id INT,
            season_id INT,
            home_team_id INT,
            away_team_id INT,
            home_score INT,
            away_score INT,
            match_status VARCHAR(20),
            match_week INT,
            competition_stage_id INT,
            stadium_id INT,
            referee_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("matches database table created")

    #create the Managers table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Managers (
            manager_id INT PRIMARY KEY,
            name VARCHAR(40),
            nickname VARCHAR(40),
            dob VARCHAR(20),
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Managers database table created")

    #create the Match-Managers table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Match_Managers (
            id SERIAL PRIMARY KEY,
            match_id INT,
            manager_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Match-Managers database table created")

    #create the Teams table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Teams (
            team_id INT PRIMARY KEY,
            team_gender VARCHAR(20),
            team_name VARCHAR(30),
            team_group VARCHAR(20),
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("teams database table created")

    #create the matches table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Referees (
            referee_id INT PRIMARY KEY,
            name VARCHAR(40),
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("referees database table created")

    #create the matches table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Stadiums (
            stadium_id INT PRIMARY KEY,
            stadium_name VARCHAR(40),
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("stadiums database table created")

    #create the matches table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Countries (
            country_id INT PRIMARY KEY,
            country_name VARCHAR(20)
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("countries database table created")

    #create the Lineups table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Lineups (
            lineup_id SERIAL PRIMARY KEY,
            match_id INT,
            team_id INT,
            team_name VARCHAR(50),
            player_id INT,
            player_name VARCHAR(50),
            player_nickname VARCHAR(50),
            jersey_number INT,
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("lineups database table created")

    #create the Cards table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Cards (
            card_id SERIAL PRIMARY KEY,
            match_id INT,
            player_id INT,
            time VARCHAR(20),
            card_type VARCHAR(20),
            reason VARCHAR(20),
            period INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Cards database table created")

    #create the Positions table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Positions (
            position_id SERIAL PRIMARY KEY,
            match_id INT,
            player_id INT,
            position VARCHAR(40),
            from_time VARCHAR(10),
            to_time VARCHAR(10),
            from_period INT,
            to_period INT,
            start_reason VARCHAR(40),
            end_reason VARCHAR(40)
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Positions database table created")

    #commit the changes
    conn.commit()
    cursor.close()
    conn.close()
    
except psycopg.OperationalError as e:
    print(f"Error: {e}")
    exit(1)