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
            home_team_manager_id INT,
            away_team_id INT,
            away_team_manager_id INT, 
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

    #execute the SQL statement
    #cursor.execute(insert_data_query)
    #print("Data inserted into table")

    #commit the changes
    conn.commit()
    cursor.close()
    conn.close()
    
except psycopg.OperationalError as e:
    print(f"Error: {e}")
    exit(1)