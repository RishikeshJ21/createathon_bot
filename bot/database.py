import psycopg2
import os
import math
from psycopg2.extras import DictCursor

# Fetch database credentials from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# Ensure all environment variables are loaded
if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
    raise ValueError("Missing one or more environment variables: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST")

# Initialize database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        cursor_factory=DictCursor
    )

# Initialize the database and create the User table
def initialize_database():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS public."User" (
                chart_id SERIAL PRIMARY KEY,
                first_name TEXT,
                email TEXT UNIQUE,
                insta_id TEXT,
                telegram_id TEXT,
                youtube_id TEXT
            );
            """)
            conn.commit()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.fav_video (
                insta_id character varying,
                insta_url character varying NOT NULL,
                tele_user character varying NOT NULL,
                youtube_id character varying,
                youtube_url character varying,
                CONSTRAINT fav_video_pkey PRIMARY KEY (insta_url, tele_user)
            );
            """)
            conn.commit()

# Save user information into the "User" table
def save_user_info(user_data):
    query = """
    INSERT INTO public."User" (chart_id, first_name, email, insta_id, telegram_id, youtube_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (email) DO UPDATE
    SET first_name = EXCLUDED.first_name,
        insta_id = EXCLUDED.insta_id,
        telegram_id = EXCLUDED.telegram_id,
        youtube_id = EXCLUDED.youtube_id;
    """
    execute_query(query, (
        user_data['chart_id'],
        user_data['first_name'],
        user_data['email'],
        user_data.get('insta_id'),
        user_data.get('telegram_id'),
        user_data.get('youtube_id')
    ))

# Save Instagram data into the "instagram" table
def save_instagram_info(instagram_data):
    query = """
    INSERT INTO public.instagram (username, email, name, followers, following, profile)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (email) DO UPDATE
    SET username = EXCLUDED.username,
        name = EXCLUDED.name,
        followers = EXCLUDED.followers,
        following = EXCLUDED.following,
        profile = EXCLUDED.profile;
    """
    execute_query(query, (
        instagram_data['username'],
        instagram_data['email'],
        instagram_data['name'],
        instagram_data['followers'],
        instagram_data['following'],
        instagram_data['profile']
    ))

# Save video information into the "fav_video" table
def save_video_info(video_data):
    query = """
    INSERT INTO public.fav_video (insta_id, insta_url, tele_user, youtube_id, youtube_url)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (insta_id) DO UPDATE
    SET insta_url = EXCLUDED.insta_url,
        tele_user = EXCLUDED.tele_user,
        youtube_id = EXCLUDED.youtube_id,
        youtube_url = EXCLUDED.youtube_url;
    """
    execute_query(query, (
        video_data.get('insta_id'),
        video_data['insta_url'],
        video_data['tele_user'],
        video_data.get('youtube_id'),
        video_data.get('youtube_url')
    ))

# Fetch the 'rules' from the 'guide' table
def fetch_guide_rules():
    query = "SELECT rules FROM public.guide;"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()  # Use fetchall to get all rows
                
                if result:
                    # Create a bullet-pointed list of rules
                    rules_list = "\n".join([f"• {row['rules']}" for row in result])  # Format each rule with a bullet point
                    return rules_list
                else:
                    return "No rules found."
    except Exception as e:
        print(f"Failed to fetch guide rules: {e}")
        return "Error fetching rules."


# Fetch challenges from the 'challengers' table
def fetch_challenges():
    query = """
    SELECT id, challenge_name, task, links, taskon, duration, prize, "timestamp", challenge_task
    FROM public.challengers;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                # Convert the result to a list of dictionaries for easier handling
                challenges = []
                for row in results:
                    challenge = {
                        'id': row['id'],
                        'challenge_name': row['challenge_name'],
                        'task': row['task'],
                        'links': row['links'],
                        'taskon': row['taskon'],
                        'duration': row['duration'],
                        'prize': row['prize'],
                        'timestamp': row['timestamp'],
                        'challenge_task': row['challenge_task']
                    }
                    challenges.append(challenge)
                return challenges
    except Exception as e:
        print(f"Failed to fetch challenges: {e}")
        return None

# Fetch a single challenge by its ID from the 'challengers' table
def fetch_challenge_by_id(challenge_id):
    query = """
    SELECT id, challenge_name, task, links, taskon, duration, prize, "timestamp", challenge_task
    FROM public.challengers
    WHERE id = %s;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (challenge_id,))
                result = cursor.fetchone()
                if result:
                    # Convert the result to a dictionary
                    challenge = {
                        'id': result['id'],
                        'challenge_name': result['challenge_name'],
                        'task': result['task'],
                        'links': result['links'],
                        'taskon': result['taskon'],
                        'duration': result['duration'],
                        'prize': result['prize'],
                        'timestamp': result['timestamp'],
                        'challenge_task': result['challenge_task']
                    }
                    
                    return challenge
                else:
                    print(f"No challenge found with ID: {challenge_id}")
                    return None
    except Exception as e:
        print(f"Failed to fetch challenge by ID {challenge_id}: {e}")
        return None


def upload_task_progress(progresstrack_data):
    query = """
    INSERT INTO public.progresstrack (user_id, challenge_id, submit, day, link, challenge_day_id, submition_day)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    ON CONFLICT (id) DO UPDATE
    SET user_id = EXCLUDED.user_id,
        challenge_id = EXCLUDED.challenge_id,
        submit = EXCLUDED.submit,
        day = EXCLUDED.day,
        link = EXCLUDED.link,
        challenge_day_id = EXCLUDED.challenge_day_id,
        submition_day = NOW();
    """
    
    execute_query(query, (
        progresstrack_data['user_id'],
        progresstrack_data['challenge_id'],
        progresstrack_data['submit'],
        progresstrack_data['day'],
        progresstrack_data['link'],
        progresstrack_data['challenge_day_id']
    ))


def upload_task_progress_checker(progresstrack_data):
    # Check if the progress already exists
    existing_progress = check_if_task_completed(progresstrack_data['challenge_id'], progresstrack_data['day'], progresstrack_data['user_id'])
    
    if existing_progress:
        # If progress already exists, return a message or skip the insertion
        print(f"Progress for Challenge ID {progresstrack_data['challenge_id']} on Day {progresstrack_data['day']} already exists.")
        return False  # Return False indicating the progress is already uploaded
    
    # If progress doesn't exist, insert or update the record
    query = """
    INSERT INTO public.progresstrack (user_id, challenge_id, submit, day, link, challenge_day_id, submition_day)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    ON CONFLICT (id) DO UPDATE
    SET user_id = EXCLUDED.user_id,
        challenge_id = EXCLUDED.challenge_id,
        submit = EXCLUDED.submit,
        day = EXCLUDED.day,
        link = EXCLUDED.link,
        challenge_day_id = EXCLUDED.challenge_day_id,
        submition_day = NOW();
    """
    
    execute_query(query, (
        progresstrack_data['user_id'],
        progresstrack_data['challenge_id'],
        progresstrack_data['submit'],
        progresstrack_data['day'],
        progresstrack_data['link'],
        progresstrack_data['challenge_day_id']
    ))

    return True  # Return True indicating the progress has been uploaded successfully
def check_if_task_completed(challenge_id, day, user_id):
    query = """
    SELECT 1 FROM public.progresstrack
    WHERE user_id = %s AND challenge_id = %s AND day = %s
    LIMIT 1;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, challenge_id, day))
                result = cursor.fetchone()  # Returns a tuple or None if no record exists
                return result is not None  # Return True if the task exists, otherwise False
    except Exception as e:
        print(f"Failed to check task completion for challenge {challenge_id}, day {day}, user {user_id}: {e}")
        return False  # Return False if there is an issue

def get_total_days_for_challenge(challenge_id):
    query = """
    SELECT challenge_task
    FROM public.challengers
    WHERE id = %s
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (challenge_id,))
                result = cursor.fetchone()  # Fetch result as tuple or None if no record exists
                
                if result:
                    # Parse the challenge_task JSON (assuming it's a JSON structure)
                    challenge_task = result[0]
                    # Count the number of days (keys like "Day1", "Day2", etc.)
                    return len(challenge_task)
                else:
                    return 0  # Return 0 if no challenge exists with the provided ID
    except Exception as e:
        print(f"Failed to fetch tasks for challenge {challenge_id}: {e}")
        return 0  # Return 0 if there's an error with fetching the challenge
def get_completed_days_for_user(challenge_id, user_id):
    # Query to count how many distinct days (challenge_day_id) a user has completed for the given challenge_id and user_id
    query = """
    SELECT COUNT(DISTINCT challenge_day_id) AS completed_days, MAX(submition_day) AS last_submission_date
    FROM public.progresstrack
    WHERE challenge_id = %s AND user_id = %s AND submit = TRUE
    GROUP BY challenge_id, user_id;
    """
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (challenge_id, user_id))
                result = cursor.fetchone()  # Fetch the result as a tuple or None if no record found
                
                if result:
                    completed_days = result[0]  # Number of completed days (count of distinct challenge_day_id)
                    return completed_days # Return completed days and last submission date
                else:
                    return 0, None  # Return 0 if no completed tasks are found and None for the date
                
    except Exception as e:
        print(f"Failed to fetch completed days for challenge {challenge_id}, user {user_id}: {e}")
        return 0, None  # Return 0 and None in case of an error

def save_winner(winner_data):
    query = """
    INSERT INTO public.winners (challenge_id, user_id, status)
    VALUES (%s, %s, %s)
    ON CONFLICT (id) DO UPDATE
    SET challenge_id = EXCLUDED.challenge_id,
        user_id = EXCLUDED.user_id,
        status = EXCLUDED.status;
    """
    
    execute_query(query, (
        winner_data['challenge_id'],
        winner_data['user_id'],
        winner_data['status']
    ))

def execute_query(query, params=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
    except Exception as e:
        print(f"Database operation failed: {e}")

# Initialize the database
if __name__ == "__main__":
    initialize_database()
