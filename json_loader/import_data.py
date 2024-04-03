import json
import os
import shutil
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
    match_ids = []
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
            match_ids.append(match['match_id'])
    conn.commit()
    return match_ids

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

# Function to insert data into the Events table
def insert_into_events(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        # Check if the event already exists in the table
        cursor.execute("SELECT 1 FROM Events WHERE event_id = %s", (event['id'],))
        existing_event = cursor.fetchone()
        if not existing_event:
            out = event['out'] if event.get('out') is not None else None
            player = event['player']['id'] if event.get('player') is not None else None
            if event.get('position') is not None: 
                position_id = event['position']['id']
                position_name = event['position']['name']
            else:
                position_id = None
                position_name = None
            off_camera = event['off_camera'] if event.get('off_camera') is not None else None
            under_pressure = event['under_pressure'] if event.get('under_pressure') is not None else None
            tactics_formation = event['tactics']['formation'] if event.get('tactics') is not None else None
            location = event['location'] if event.get('location') is not None else None
            duration = event['duration'] if event.get('duration') is not None else None
            cursor.execute("""
                INSERT INTO Events (event_id, match_id, index, period, timestamp, minute, second, 
                type_id, type_name, possession, possession_team_id, play_pattern_id, play_pattern_name, 
                team_id, player_id, position_id, position_name, location, duration, 
                under_pressure, off_camera, out, tactics_formation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (event['id'], match, event['index'], event['period'], event['timestamp'], event['minute'], event['second'],
                 event['type']['id'], event['type']['name'], event['possession'], event['possession_team']['id'],
                 event['play_pattern']['id'], event['play_pattern']['name'],
                 event['team']['id'], player, position_id, position_name, 
                 location, duration, under_pressure, off_camera, out, tactics_formation)
            )
    conn.commit()

# Function to insert data into the Passes table
def insert_into_passes(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('pass') is not None:
            _pass = event['pass']
            recipient_id = _pass['recipient']['id'] if _pass.get('recipient') is not None else None
            height_id = _pass['height']['id'] if _pass.get('height') is not None else None
            height_name = _pass['height']['name'] if _pass.get('height') is not None else None
            through_ball = _pass['through_ball'] if _pass.get('through_ball') is not None else None
            assisted_shot_id = _pass['assisted_shot_id'] if _pass.get('assisted_shot_id') is not None else None
            shot_assist = _pass['shot_assist'] if _pass.get('shot_assist') is not None else None
            goal_assist = _pass['goal_assist'] if _pass.get('goal_assist') is not None else None
            backheel = _pass['backheel'] if _pass.get('backheel') is not None else None
            deflected = _pass['deflected'] if _pass.get('deflected') is not None else None
            miscommunication = _pass['miscommunication'] if _pass.get('miscommunication') is not None else None
            cross = _pass['cross'] if _pass.get('cross') is not None else None
            cutback = _pass['cutback'] if _pass.get('cutback') is not None else None
            switch = _pass['switch'] if _pass.get('switch') is not None else None
            technique_id = _pass['technique']['id'] if _pass.get('technique') is not None else None
            technique_name = _pass['technique']['name'] if _pass.get('technique') is not None else None
            outcome_id = _pass['outcome']['id'] if _pass.get('outcome') is not None else None
            outcome_name = _pass['outcome']['name'] if _pass.get('outcome') is not None else None
            body_part_id = _pass['body_part']['id'] if _pass.get('body_part') is not None else None
            body_part_name = _pass['body_part']['name'] if _pass.get('body_part') is not None else None
            cursor.execute("""
                    INSERT INTO Passes (event_id, match_id, recipient_id, length, angle, height_id,
                    height_name, through_ball, end_location, body_part_id, body_part_name, assisted_shot_id, shot_assist,
                    goal_assist, backheel, deflected, miscommunication, cross_, cutback, switch, technique_id,
                    technique_name, outcome_id, outcome_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, recipient_id, _pass['length'], _pass['angle'], height_id, height_name, through_ball, 
                     _pass['end_location'], body_part_id, body_part_name, assisted_shot_id,
                     shot_assist, goal_assist, backheel, deflected, miscommunication, cross, cutback, switch, technique_id,
                     technique_name, outcome_id, outcome_name)
                )
    conn.commit()

# Function to insert data into the Shots table
def insert_into_shots(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('shot') is not None:
            shot = event['shot']
            deflected = shot['deflected'] if shot.get('deflected') is not None else None
            aerial_won = shot['aerial_won'] if shot.get('aerial_won') is not None else None
            follows_dribble = shot['follows_dribble'] if shot.get('follows_dribble') is not None else None
            first_time = shot['first_time'] if shot.get('first_time') is not None else None
            open_goal = shot['open_goal'] if shot.get('open_goal') is not None else None
            statsbomb_xg = shot['statsbomb_xg'] if shot.get('statsbomb_xg') is not None else None
            key_pass_id = shot['key_pass_id'] if shot.get('key_pass_id') is not None else None
            cursor.execute("""
                    INSERT INTO Shots (event_id, match_id, end_location, key_pass_id, statsbomb_xg, technique_id, technique_name,
                    outcome_id, outcome_name, type_id, type_name, body_part_id, body_part_name, deflected, aerial_won, follows_dribble,
                    first_time, open_goal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, shot['end_location'], key_pass_id, statsbomb_xg, shot['technique']['id'],
                     shot['technique']['name'], shot['outcome']['id'], shot['outcome']['name'], shot['type']['id'], shot['type']['name'], 
                     shot['body_part']['id'], shot['body_part']['name'], deflected, aerial_won, follows_dribble, first_time, open_goal)
                )
    conn.commit()

# Function to insert data into the Duels table
def insert_into_duels(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('duel') is not None:
            duel = event['duel']
            counterpress = duel['counterpress'] if duel.get('counterpress') is not None else None
            outcome_id = duel['outcome']['id'] if duel.get('outcome') is not None else None
            outcome_name = duel['outcome']['name'] if duel.get('outcome') is not None else None
            cursor.execute("""
                    INSERT INTO Duels (event_id, match_id, type_id, type_name, outcome_id, outcome_name, counterpress)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, duel['type']['id'], duel['type']['name'], outcome_id, outcome_name, counterpress)
                )
    conn.commit()

# Function to insert data into the Dribbles table
def insert_into_dribbles(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('dribble') is not None:
            dribble = event['dribble']
            overrun = dribble['overrun'] if dribble.get('overrun') is not None else None
            nutmeg = dribble['nutmeg'] if dribble.get('nutmeg') is not None else None
            no_touch = dribble['no_touch'] if dribble.get('no_touch') is not None else None
            cursor.execute("""
                    INSERT INTO Dribbles (event_id, match_id, outcome_id, outcome_name, overrun, nutmeg, no_touch)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, dribble['outcome']['id'], dribble['outcome']['name'], overrun, nutmeg, no_touch)
                )
    conn.commit()
            
# Function to insert data into the Blocks table
def insert_into_blocks(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('block') is not None:
            block = event['block']
            deflection = block['deflection'] if block.get('deflection') is not None else None
            save_block = block['save_block'] if block.get('save_block') is not None else None
            offensive = block['offensive'] if block.get('offensive') is not None else None
            counterpress = block['counterpress'] if block.get('counterpress') is not None else None
            cursor.execute("""
                    INSERT INTO Blocks (event_id, match_id, deflection, save_block, offensive, counterpress)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, deflection, save_block, offensive, counterpress)
                )
    conn.commit()

# Function to insert data into the Goalkeeper table
def insert_into_goalkeeper(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('goalkeeper') is not None:
            keeper = event['goalkeeper']
            end_location = keeper['end_location'] if keeper.get('end_location') is not None else None
            technique_id = keeper['technique_id'] if keeper.get('technique_id') is not None else None
            technique_name = keeper['technique_name'] if keeper.get('technique_name') is not None else None
            outcome_id = keeper['outcome_id'] if keeper.get('outcome_id') is not None else None
            outcome_name = keeper['outcome_name'] if keeper.get('outcome_name') is not None else None
            body_part_id = keeper['body_part_id'] if keeper.get('body_part_id') is not None else None
            body_part_name = keeper['body_part_name'] if keeper.get('body_part_name') is not None else None
            position_id = keeper['position']['id'] if keeper.get('position') is not None else None
            position_name = keeper['position']['name'] if keeper.get('position') is not None else None
            cursor.execute("""
                    INSERT INTO Goalkeeper (event_id, match_id, technique_id, technique_name, position_id, position_name, type_id, type_name,
                    outcome_id, outcome_name, body_part_id, body_part_name, end_location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, technique_id, technique_name, position_id, position_name, keeper['type']['id'],
                     keeper['type']['name'], outcome_id, outcome_name, body_part_id, body_part_name, end_location)
                )
    conn.commit()

# Function to insert data into the Substitutions table
def insert_into_substitutions(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('substitution') is not None:
            sub = event['substitution']
            cursor.execute("""
                    INSERT INTO Substitutions (event_id, match_id, outcome_id, outcome_name, replacement_id, replacement_name)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, sub['outcome']['id'], sub['outcome']['name'], sub['replacement']['id'], sub['replacement']['name'])
                )
    conn.commit()

# Function to insert data into the Foul_Committed table
def insert_into_foul_committed(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('foul_committed') is not None:
            foul = event['foul_committed']
            offensive = foul['offensive'] if foul.get('offensive') is not None else None
            advantage = foul['advantage'] if foul.get('advantage') is not None else None
            penalty = foul['penalty'] if foul.get('penalty') is not None else None
            type_id = foul['type']['id'] if foul.get('type') is not None else None
            type_name = foul['type']['name'] if foul.get('type') is not None else None
            card_id = foul['card']['id'] if foul.get('card') is not None else None
            card_name = foul['card']['name'] if foul.get('card') is not None else None
            counterpress = foul['counterpress'] if foul.get('counterpress') is not None else None
            cursor.execute("""
                    INSERT INTO Foul_Committed (event_id, match_id, offensive, advantage, penalty, type_id, type_name, card_id, card_name, counterpress)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (event['id'], match, offensive, advantage, penalty, type_id, type_name, card_id, card_name, counterpress)
                )
    conn.commit()

# Function to insert data into the Foul_Won table
def insert_into_foul_won(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('foul_won') is not None:
            foul = event['foul_won']
            defensive = foul['defensive'] if foul.get('defensive') is not None else None
            advantage = foul['advantage'] if foul.get('advantage') is not None else None
            penalty = foul['penalty'] if foul.get('penalty') is not None else None
            cursor.execute("""
                    INSERT INTO Foul_Won (event_id, match_id, defensive, advantage, penalty)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (event['id'], match, defensive, advantage, penalty)
                )
    conn.commit()

# Function to insert data into the Foul_Won table
def insert_into_50_50(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('50-50') is not None:
            _50_50 = event['50-50']
            outcome_id = _50_50['outcome']['id'] if _50_50.get('outcome') is not None else None
            outcome_name = _50_50['outcome']['name'] if _50_50.get('outcome') is not None else None
            counterpress = _50_50['counterpress'] if _50_50.get('counterpress') is not None else None
            cursor.execute("""
                    INSERT INTO _50_50 (event_id, match_id, outcome_id, outcome_name, counterpress)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (event['id'], match, outcome_id, outcome_name, counterpress)
                )
    conn.commit()

# Function to insert data into the Carry table
def insert_into_carry(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('carry') is not None:
            carry = event['carry']
            end_location = carry['end_location'] if carry.get('end_location') is not None else None
            cursor.execute("""
                    INSERT INTO Carry (event_id, match_id, end_location)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, end_location)
                )
    conn.commit()

# Function to insert data into the Clearance table
def insert_into_clearance(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('clearance') is not None:
            clearance = event['clearance']
            aerial_won = clearance['aerial_won'] if clearance.get('aerial_won') is not None else None
            body_part_id = clearance['body_part']['id'] if clearance.get('body_part') is not None else None
            body_part_name = clearance['body_part']['name'] if clearance.get('body_part') is not None else None
            cursor.execute("""
                    INSERT INTO Clearance (event_id, match_id, aerial_won, body_part_id, body_part_name)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (event['id'], match, aerial_won, body_part_id, body_part_name)
                )
    conn.commit()

# Function to insert data into the Dribbled_Past table
def insert_into_dribbled_past(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('dribbled_past') is not None:
            dribble = event['dribbled_past']
            counterpress = dribble['counterpress'] if dribble.get('counterpress') is not None else None
            cursor.execute("""
                    INSERT INTO Dribbled_Past (event_id, match_id, counterpress)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, counterpress)
                )
    conn.commit()

# Function to insert data into the Bad_Behaviour table
def insert_into_bad_behaviour(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('bad_behaviour') is not None:
            bad = event['bad_behaviour']
            card_id = bad['card']['id'] if bad.get('card') is not None else None
            card_name = bad['card']['name'] if bad.get('card') is not None else None
            cursor.execute("""
                    INSERT INTO Bad_Behaviour (event_id, match_id, card_id, card_name)
                    VALUES (%s, %s, %s, %s)""",
                    (event['id'], match, card_id, card_name)
                )
    conn.commit()

# Function to insert data into the Ball_Receipt table
def insert_into_ball_receipt(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('ball_receipt') is not None:
            ball = event['ball_receipt']
            outcome_id = ball['outcome']['id'] if ball.get('outcome') is not None else None
            outcome_name = ball['outcome']['name'] if ball.get('outcome') is not None else None
            cursor.execute("""
                    INSERT INTO Ball_Receipt (event_id, match_id, outcome_id, outcome_name)
                    VALUES (%s, %s, %s, %s)""",
                    (event['id'], match, outcome_id, outcome_name)
                )
    conn.commit()

# Function to insert data into the Ball_Recovery table
def insert_into_ball_recovery(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('ball_recovery') is not None:
            ball = event['ball_recovery']
            offensive = ball['offensive'] if ball.get('offensive') is not None else None
            cursor.execute("""
                    INSERT INTO Ball_Recovery (event_id, match_id, offensive)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, offensive)
                )
    conn.commit()

# Function to insert data into the Injury_Stoppage table
def insert_into_injury_stoppage(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('injury_stoppage') is not None:
            injury = event['injury_stoppage']
            in_chain = injury['in_chain'] if injury.get('in_chain') is not None else None
            cursor.execute("""
                    INSERT INTO Injury_Stoppage (event_id, match_id, in_chain)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, in_chain)
                )
    conn.commit()


# Function to insert data into the Interception table
def insert_into_interception(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('interception') is not None:
            interception = event['interception']
            outcome_id = interception['outcome']['id'] if interception.get('outcome') is not None else None
            outcome_name = interception['outcome']['name'] if interception.get('outcome') is not None else None
            cursor.execute("""
                    INSERT INTO Interception (event_id, match_id, outcome_id, outcome_name)
                    VALUES (%s, %s, %s, %s)""",
                    (event['id'], match, outcome_id, outcome_name)
                )
    conn.commit()

# Function to insert data into the Miscontrol table
def insert_into_miscontrol(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('miscontrol') is not None:
            mis = event['miscontrol']
            aerial_won = mis['aerial_won'] if mis.get('aerial_won') is not None else None
            cursor.execute("""
                    INSERT INTO Miscontrol (event_id, match_id, aerial_won)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, aerial_won)
                )
    conn.commit()

# Function to insert data into the Player_Off table
def insert_into_player_off(conn, event_data, match):
    cursor = conn.cursor()
    for event in event_data:
        if event.get('player_off') is not None:
            player = event['player_off']
            perm = player['permanent'] if player.get('permanent') is not None else None
            cursor.execute("""
                    INSERT INTO Player_Off (event_id, match_id, permanent)
                    VALUES (%s, %s, %s)""",
                    (event['id'], match, perm)
                )
    conn.commit()

# Function to parse Match JSON data and insert into tables
def insert_match_data_from_json(conn, json_file):
    matches = []
    with open(json_file, 'r', encoding="utf-8") as f:
        match_data = json.load(f)
        matches.append(insert_into_matches(conn, match_data))
        insert_into_managers(conn, match_data)
        insert_into_teams(conn, match_data)
        insert_into_referees(conn, match_data)
        insert_into_stadiums(conn, match_data)
    return matches

# Function to parse Competition JSON data and insert into tables
def insert_competition_data_from_json(conn, json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        competition_data = json.load(f)
        insert_into_competitions(conn, competition_data)

# Function to parse Lineups JSON data and insert into tables
def insert_lineup_data_from_json(conn, json_file, filename):
    with open(json_file, 'r', encoding="utf-8") as file:
        lineup_data = json.load(file)
        match_id = filename.split('.')[0]
        insert_into_lineups(conn, lineup_data, match_id)
        insert_into_cards(conn, lineup_data, match_id)
        insert_into_positions(conn, lineup_data, match_id)

# Function to parse Events JSON data and insert into tables
def insert_event_data_from_json(conn, json_file, filename):
    with open(json_file, 'r', encoding="utf-8") as file:
        event_data = json.load(file)
        match_id = filename.split('.')[0]
        insert_into_events(conn, event_data, match_id)
        insert_into_passes(conn, event_data, match_id)
        insert_into_shots(conn, event_data, match_id)
        insert_into_duels(conn, event_data, match_id)
        insert_into_dribbles(conn, event_data, match_id)
        insert_into_blocks(conn, event_data, match_id)
        insert_into_goalkeeper(conn, event_data, match_id)
        insert_into_substitutions(conn, event_data, match_id)
        insert_into_foul_committed(conn, event_data, match_id)
        insert_into_foul_won(conn, event_data, match_id)
        insert_into_50_50(conn, event_data, match_id)
        insert_into_carry(conn, event_data, match_id)
        insert_into_clearance(conn, event_data, match_id)
        insert_into_dribbled_past(conn, event_data, match_id)
        insert_into_bad_behaviour(conn, event_data, match_id)
        insert_into_ball_receipt(conn, event_data, match_id)
        insert_into_ball_recovery(conn, event_data, match_id)
        insert_into_injury_stoppage(conn, event_data, match_id)
        insert_into_interception(conn, event_data, match_id)
        insert_into_miscontrol(conn, event_data, match_id)
        insert_into_player_off(conn, event_data, match_id)

# Main function
def main():
    conn = connect_to_database()
    # Matches
    match_ids = []
    json_file = "json_loader\\Data\\matches\\11\\4.json"  # Path to JSON file La Liga 18/19
    match_ids.extend(insert_match_data_from_json(conn, json_file))
    json_file = "json_loader\\Data\\matches\\11\\42.json"  # Path to JSON file La Liga 19/20
    match_ids.extend(insert_match_data_from_json(conn, json_file))
    json_file = "json_loader\\Data\\matches\\11\\90.json"  # Path to JSON file La Liga 20/21
    match_ids.extend(insert_match_data_from_json(conn, json_file))
    json_file = "json_loader\\Data\\matches\\2\\44.json"  # Path to JSON file Premier League 03/04
    match_ids.extend(insert_match_data_from_json(conn, json_file))

    #Competitions
    competition_json_file = "json_loader\\Data\\competitions.json"
    insert_competition_data_from_json(conn, competition_json_file)
    
    #Lineups 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'Data', 'Lineups')
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_match_id = int(filename.split('.')[0])
            for m in match_ids:
                if file_match_id in m:
                    file_path = os.path.join(folder_path, filename)
                    insert_lineup_data_from_json(conn, file_path, filename)

    #Events 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'Data', 'Events')
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_match_id = int(filename.split('.')[0])
            for m in match_ids:
                if file_match_id in m:
                    file_path = os.path.join(folder_path, filename)
                    insert_event_data_from_json(conn, file_path, filename)

    conn.close()
    print("Data imported")


if __name__ == "__main__":
    main()
