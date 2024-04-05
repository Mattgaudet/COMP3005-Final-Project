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

    #create the Countries table
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
            player_id INT
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

    #create the Players table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Players (
            player_id INT PRIMARY KEY,
            player_name TEXT,
            player_nickname TEXT,
            jersey_number INT,
            country_id INT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)

    #create the Events table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Events (
            event_id VARCHAR(100) PRIMARY KEY,
            match_id INT,
            index INT,
            period INT,
            timestamp VARCHAR(20),
            minute INT,
            second INT,
            type_id INT,
            type_name VARCHAR(30),
            possession INT,
            possession_team_id INT,
            play_pattern_id INT,
            play_pattern_name VARCHAR(30),
            team_id INT,
            player_id INT,
            position_id INT,
            location VARCHAR(30),
            duration VARCHAR(20),
            under_pressure BOOLEAN,
            off_camera BOOLEAN,
            out BOOLEAN,
            tactics_formation TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Events database table created")

    #create the Passes table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Passes (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            index INT,
            period INT,
            timestamp VARCHAR(20),
            minute INT,
            second INT,
            type_id INT,
            possession INT,
            possession_team_id INT,
            play_pattern_id INT,
            play_pattern_name VARCHAR(30),
            team_id INT,
            player_id INT,
            position_id INT,
            location VARCHAR(30),
            duration VARCHAR(20),
            under_pressure BOOLEAN,
            off_camera BOOLEAN,
            out BOOLEAN,
            recipient_id INT,
            length NUMERIC(12, 8),
            angle NUMERIC(12, 8),
            height_id INT,
            height_name TEXT,
            through_ball BOOLEAN,
            end_location VARCHAR(20),
            body_part_id INT,
            body_part_name TEXT,
            assisted_shot_id VARCHAR(100),
            shot_assist BOOLEAN,
            goal_assist BOOLEAN,
            backheel BOOLEAN,
            deflected BOOLEAN,
            miscommunication BOOLEAN,
            cross_ BOOLEAN,
            cutback BOOLEAN,
            switch BOOLEAN,
            technique_id INT,
            technique_name TEXT,
            outcome_id INT,
            outcome_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Passes database table created")

    #create the Shots table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Shots (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            end_location VARCHAR(20),
            key_pass_id VARCHAR(100),
            statsbomb_xg NUMERIC(13, 9),
            technique_id INT,
            technique_name TEXT,
            outcome_id INT,
            outcome_name TEXT,
            type_id INT,
            type_name TEXT,
            body_part_id INT,
            body_part_name TEXT,
            deflected BOOLEAN,
            aerial_won BOOLEAN,
            follows_dribble BOOLEAN,
            first_time BOOLEAN,
            open_goal BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Shots database table created")

    #create the Duels table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Duels (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            type_id INT,
            type_name TEXT,
            outcome_id INT,
            outcome_name TEXT,
            counterpress BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Duels database table created")

    #create the Dribbles table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Dribbles (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            outcome_id INT,
            outcome_name TEXT,
            overrun BOOLEAN,
            nutmeg BOOLEAN,
            no_touch BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Dribbles database table created")

    #create the Blocks table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Blocks (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            deflection BOOLEAN,
            save_block BOOLEAN,
            offensive BOOLEAN,
            counterpress BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Blocks database table created")

    #create the Goalkeeper table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Goalkeeper (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            technique_id INT,
            technique_name TEXT,
            position_id INT,
            position_name TEXT,
            type_id INT,
            type_name TEXT,
            outcome_id INT,
            outcome_name TEXT,
            body_part_id INT,
            body_part_name TEXT,
            end_location VARCHAR(20)
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Goalkeeper database table created")

    #create the Substitutions table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Substitutions (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            outcome_id INT,
            outcome_name TEXT,
            replacement_id INT,
            replacement_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Substitutions database table created")

    #create the Foul_Committed table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Foul_Committed (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            offensive BOOLEAN,
            advantage BOOLEAN,
            penalty BOOLEAN,
            type_id INT,
            type_name TEXT,
            card_id INT,
            card_name TEXT,
            counterpress BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Foul_Committed database table created")

    #create the Foul_Won table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Foul_Won (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            defensive BOOLEAN,
            advantage BOOLEAN,
            penalty BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Foul_Won database table created")

    #create the _50_50 table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS _50_50 (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            outcome_id INT,
            outcome_name TEXT,
            counterpress BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("_50_50 database table created")

    #create the Carry table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Carry (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            index INT,
            period INT,
            timestamp VARCHAR(20),
            minute INT,
            second INT,
            type_id INT,
            type_name VARCHAR(30),
            possession INT,
            possession_team_id INT,
            play_pattern_id INT,
            play_pattern_name VARCHAR(30),
            team_id INT,
            player_id INT,
            position_id INT,
            location VARCHAR(30),
            duration VARCHAR(20),
            under_pressure BOOLEAN,
            off_camera BOOLEAN,
            out BOOLEAN,
            end_location VARCHAR(30)
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Carry database table created")

    #create the Clearance table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Clearance (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            aerial_won BOOLEAN,
            body_part_id INT,
            body_part_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Clearance database table created")

    #create the Dribbled_Past table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Dribbled_Past (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            counterpress BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Dribbled_Past database table created")

    #create the Bad_Behavior table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Bad_Behaviour (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            card_id INT,
            card_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Bad_Behavior database table created")

    #create the Ball_Receipt table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Ball_Receipt (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            outcome_id INT,
            outcome_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Ball_Receipt database table created")

    #create the Ball_Recovery table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Ball_Recovery (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            offensive BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Ball_Recovery database table created")

    #create the Injury_Stoppage table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Injury_Stoppage (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            in_chain BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Injury_Stoppage database table created")

    #create the Interception table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Interception (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            outcome_id INT,
            outcome_name TEXT
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Interception database table created")

    #create the Miscontrol table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Miscontrol (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            aerial_won BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Miscontrol database table created")

    #create the Player_Off table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Player_Off (
            event_id VARCHAR(50) PRIMARY KEY,
            match_id INT,
            permanent BOOLEAN
        );
        '''
    #execute the SQL statement
    cursor.execute(create_table_query)
    print("Player_Off database table created")

    #commit the changes
    conn.commit()
    cursor.close()
    conn.close()
    
except psycopg.OperationalError as e:
    print(f"Error: {e}")
    exit(1)