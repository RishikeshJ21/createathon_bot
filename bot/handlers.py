import os
import requests
from telebot import TeleBot, types
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from bot.database import save_user_info, save_instagram_info, save_video_info, fetch_guide_rules,fetch_challenges,upload_task_progress,check_if_task_completed,get_total_days_for_challenge,get_completed_days_for_user,save_winner
from bot.config import BOT_TOKEN

# Initialize bot
bot = TeleBot(BOT_TOKEN)
user_states = {}

@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    username = message.chat.first_name or "there"
    bot.reply_to(
        message,
        f"Hello, {username}! Welcome to the Createathon Bot! 😊\nPlease provide your email address to proceed."
    )
    user_states[message.chat.id] = {"next": "email"}

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("next") == "email")
def handle_email(message: Message):
    email = message.text.strip()
    if "@" in email and "." in email:  # Basic email validation
        user_states[message.chat.id]["email"] = email

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("YouTube", callback_data="media_youtube"),
            InlineKeyboardButton("Instagram", callback_data="media_instagram")
        )

        msg = bot.send_message(
            message.chat.id,
            "Thank you for providing your email! 😊\nPlease choose your preferred media:",
            reply_markup=markup
        )
        user_states[message.chat.id]["next"] = "media_selection"
        user_states[message.chat.id]["last_message_id"] = msg.message_id
    else:
        bot.reply_to(message, "That doesn't look like a valid email. Please try again!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("media_"))
def handle_media_selection(call):
    selected_media = call.data.split("_")[1]  # Extract "youtube" or "instagram"
    user_states[call.message.chat.id]["media"] = selected_media

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Back", callback_data="back_to_media_selection")
    )

    bot.edit_message_text(
        f"You selected {selected_media.capitalize()}! Please enter your {selected_media} username or user ID:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
    user_states[call.message.chat.id]["next"] = "media_username"

@bot.callback_query_handler(func=lambda call: call.data == "back_to_media_selection")
def back_to_media_selection(call):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("YouTube", callback_data="media_youtube"),
        InlineKeyboardButton("Instagram", callback_data="media_instagram")
    )

    bot.edit_message_text(
        "Please reselect your preferred media:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
    user_states[call.message.chat.id]["next"] = "media_selection"

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("next") == "media_username")
def handle_media_username(message: Message):
    media_username = message.text.strip()
    media_type = user_states[message.chat.id]["media"]

    # Save the username based on media type
    user_states[message.chat.id]["instagram_username"] = media_username

    if media_type == "instagram":
        # Make API call to get Instagram user info
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={media_username}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()['data']['user']
            name = user_data['full_name']
            followers = user_data['edge_followed_by']['count']
            following = user_data['edge_follow']['count']
            profile_picture = user_data['profile_pic_url_hd']

            # Save the Instagram user info to user_states for later use
            user_states[message.chat.id]["instagram_name"] = name
            user_states[message.chat.id]["instagram_followers"] = followers
            user_states[message.chat.id]["instagram_following"] = following
            user_states[message.chat.id]["instagram_profile_pic"] = profile_picture

            # Show the user their info
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("Confirm", callback_data="confirm_instagram_info"),
                InlineKeyboardButton("Edit Username", callback_data="edit_instagram_username")
            )
            
            bot.send_message(
                message.chat.id,
                f"Here is your Instagram info:\nName: {name}\nFollowers: {followers}\nFollowing: {following}\nProfile Picture: {profile_picture}",
                reply_markup=markup
            )
            user_states[message.chat.id]["next"] = "confirm_instagram_info"
            
        else:
            bot.send_message(message.chat.id, "Sorry, I couldn't fetch your Instagram info. Please try again later.")
            user_states[message.chat.id]["next"] = "media_username"
    else:
        # Handle other media types (e.g., YouTube)
        pass

@bot.callback_query_handler(func=lambda call: call.data == "confirm_instagram_info")
def confirm_instagram_info(call):
    user_id = call.message.chat.id
    instagram_username = user_states[user_id].get("instagram_username")  # Get Instagram username
    email = user_states[user_id]["email"]

    # Fetch the Instagram user info from user states
    instagram_name = user_states[user_id].get("instagram_name")
    instagram_followers = user_states[user_id].get("instagram_followers")
    instagram_following = user_states[user_id].get("instagram_following")
    instagram_profile_pic = user_states[user_id].get("instagram_profile_pic")

    # Save user info (telegram, email, etc.)
    save_user_info({
        'chart_id': user_id,
        'first_name': call.message.chat.first_name,
        'email': email,
        'telegram_id': call.message.chat.username
    })

    # Save Instagram info in the database
    save_instagram_info({
        'username': instagram_username,  # Instagram username
        'email': email,
        'name': instagram_name,  # Full name
        'followers': instagram_followers,  # Followers count
        'following': instagram_following,  # Following count
        'profile': instagram_profile_pic  # Profile picture URL
    })

    # Respond to user with success message
    bot.send_message(call.message.chat.id, "Your Instagram information has been saved successfully! 😊")
    
    # Ask for the best video URL
    bot.send_message(
        call.message.chat.id,
        "Please send us your best Reel or Video URL. If you wish to skip, press 'Skip'."
    )

    # Send the "Skip" button
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Skip", callback_data="skip_button"))

    bot.send_message(
        call.message.chat.id,
        "You can skip sending the video URL by pressing the button below.",
        reply_markup=markup
    )

    # Update user state to expect a URL or skip
    user_states[call.message.chat.id]["next"] = "video_url"


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("next") == "video_url")
def handle_video_url(message: Message):
    video_url = message.text.strip()

    # Validate the URL (basic validation for now)
    if video_url.startswith("http"):
        user_states[message.chat.id]["video_url"] = video_url

        # Retrieve user information from user states
        telegram_username = message.chat.username  # Telegram username
        instagram_username = user_states[message.chat.id].get("instagram_username")  # Instagram username

        # Save the video URL and associated data into the database
        save_video_info({
            'tele_user': telegram_username,
            'insta_id': instagram_username,
            'insta_url': video_url,
            'youtube_id': None,  # YouTube data is not provided in this case
            'youtube_url': None
        })

        bot.send_message(
            message.chat.id,
            "Thank you for sending your video URL! 😊 Your information has been successfully submitted."
        )

        # Reset user state after submission
        user_states[message.chat.id]["next"] = None

    else:
        bot.send_message(message.chat.id, "That doesn't look like a valid URL. Please send a valid video URL.")


@bot.callback_query_handler(func=lambda call: call.data == "skip_button")
def handle_skip(call):
    user_id = call.message.chat.id

    # Reset the user state to skip the URL and move forward
    user_states[user_id]["next"] = None

    bot.send_message(
        call.message.chat.id,
        "You have chosen to skip the video URL. Let's move forward."
    )

    # Provide the next steps (Guide, Challenges, etc.)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Guide", callback_data="guide_button"),
        InlineKeyboardButton("Challenges", callback_data="challenges_button")
    )

    bot.send_message(
        call.message.chat.id,
        "You can now manage your participation. Please choose an option:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("next") == "video_url")
def handle_video_url(message: Message):
    video_url = message.text.strip()

    # Validate the URL (basic validation for now)
    if video_url.startswith("http"):
        user_states[message.chat.id]["video_url"] = video_url

        # Retrieve user information from user states
        telegram_username = message.chat.username  # Telegram username
        instagram_username = user_states[message.chat.id].get("instagram_username")  # Instagram username

        # Save the video URL and associated data into the database
        save_video_info({
            'tele_user': telegram_username,
            'insta_id': instagram_username,
            'insta_url': video_url,
            'youtube_id': None,  # YouTube data is not provided in this case
            'youtube_url': None
        })

        bot.send_message(
            message.chat.id,
            "Thank you for sending your video URL! 😊 Your information has been successfully submitted."
        ) 
        InlineKeyboardButton("Skip", callback_data="skip_button")

    else:
        bot.send_message(message.chat.id, "That doesn't look like a valid URL. Please send a valid video URL.")

    # Send a new set of options: Guide, Challenges, and Skip
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Guide", callback_data="guide_button"),
        InlineKeyboardButton("Challenges", callback_data="challenges_button"),
        InlineKeyboardButton("Skip", callback_data="skip_button")
    )

    bot.send_message(
        message.chat.id,
        "You can now manage your participation. Please choose an option:",
        reply_markup=markup
    )

    # Reset the user state after submission or skipping
    user_states[message.chat.id]["next"] = None

@bot.callback_query_handler(func=lambda call: call.data == "skip_button")
def handle_skip(call):
    # When "Skip" is clicked, reset the user state and provide a response
    user_states[call.message.chat.id]["next"] = None
    bot.send_message(
        call.message.chat.id,
        "You have chosen to skip the video URL. Feel free to continue with other options."
    )
    
    # Send the same options again
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Guide", callback_data="guide_button"),
        InlineKeyboardButton("Challenges", callback_data="challenges_button")
    )

    bot.send_message(
        call.message.chat.id,
        "You can now manage your participation. Please choose an option:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "guide_button")
def guide_button_click(call):
    # Fetch the guidelines from the fetch_guide_rules function
    guidelines = fetch_guide_rules()

    # Send the guidelines to the user
    bot.send_message(call.message.chat.id, guidelines)

    # Add a back button to return to options
    back_markup = InlineKeyboardMarkup()
    back_markup.add(
        InlineKeyboardButton("Back", callback_data="back_button")
    )

    bot.send_message(
        call.message.chat.id,
        "You've read the guidelines.",
        reply_markup=back_markup
    )


# Handle the back button click event
@bot.callback_query_handler(func=lambda call: call.data == "back_button")
def back_button_click(call):
    # Send the original options: Guide and Challenges
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Guide", callback_data="guide_button"),
        InlineKeyboardButton("Challenges", callback_data="challenges_button")
    )

    bot.send_message(
        call.message.chat.id,
        
        reply_markup=markup
    )
    
    

 
    
 # Pagination function
def paginate_challenges(challenges, page=0, challenges_per_page=1):
    start = page * challenges_per_page
    end = start + challenges_per_page
    return challenges[start:end]

# Handle the button click to display challenges
@bot.callback_query_handler(func=lambda call: call.data == "challenges_button")
def challenges_button_click(call):
    display_challenges(call.message.chat.id, 0)

# Function to display challenges with pagination
def display_challenges(chat_id, page):
    
    challenges = fetch_challenges()
    
    if not challenges:
        bot.send_message(chat_id, "No challenges available.")
        return

    paginated_challenges = paginate_challenges(challenges, page)

    for challenge in paginated_challenges:
        message_text = f"""
        🏆 {challenge['challenge_name']}
        Task: {challenge['task']}
        Task Start Date: {challenge['taskon']}
        Duration: {challenge['duration']} days
        Prize: {challenge['prize']}
        Links: {challenge['links']}
        """

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Select this Challenge", callback_data=f"select_challenge_{challenge['id']}"))

        # Add pagination buttons
        if page > 0:
            markup.add(types.InlineKeyboardButton("Back", callback_data=f"back_{page - 1}"))
        if (page + 1) * 1 < len(challenges):
            markup.add(types.InlineKeyboardButton("Next", callback_data=f"next_{page + 1}"))

        bot.send_message(chat_id, message_text.strip(), reply_markup=markup)

# Handle Back and Next pagination
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_"))
def back_pagination(call):
    page = int(call.data.split("_")[1])
    display_challenges(call.message.chat.id, page)

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_"))
def next_pagination(call):
    page = int(call.data.split("_")[1])
    display_challenges(call.message.chat.id, page)

# Handle challenge selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_challenge_"))
def select_challenge_click(call):
    challenge_id = int(call.data.split("_")[2])
    challenge = next((c for c in fetch_challenges() if c['id'] == challenge_id), None)

    if not challenge:
        bot.send_message(call.message.chat.id, "Challenge not found.")
        return

    message_text = f"You've selected {challenge['challenge_name']}. Please choose a day:"
    markup = InlineKeyboardMarkup()

    for day, task_details in challenge['challenge_task'].items():
        markup.add(InlineKeyboardButton(day, callback_data=f"task_{challenge_id}_{day}"))

    # Add the "Check All Tasks Completed" button
    markup.add(InlineKeyboardButton("Check All Tasks Completed", callback_data=f"check_tasks_{challenge_id}"))

    bot.send_message(call.message.chat.id, message_text, reply_markup=markup)

# Handle day selection and display task details
@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def task_day_click(call):
    _, challenge_id, day = call.data.split("_")
    challenge = next((c for c in fetch_challenges() if c['id'] == int(challenge_id)), None)

    if not challenge:
        bot.send_message(call.message.chat.id, "Challenge not found.")
        return

    task_details = challenge['challenge_task'].get(day, None)
    if not task_details:
        bot.send_message(call.message.chat.id, f"No task found for {day}.")
        return

    message_text = f"Task for {day}: {task_details}\n\nWould you like to upload your progress?"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Upload Progress", callback_data=f"upload_{challenge_id}_{day}"))

    bot.send_message(call.message.chat.id, message_text, reply_markup=markup)

# Handle "Check All Tasks Completed" button click
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_tasks_"))
def check_tasks_completed(call):
    challenge_id = int(call.data.split("_")[2])
    user_id = call.message.chat.id

    if check_all_tasks_completed(challenge_id, user_id):
        bot.send_message(user_id, "All tasks completed! Proceed to the next step.")
        
        # Save the winner when all tasks are completed
        winner_data = {
            'challenge_id': challenge_id,
            'user_id': user_id,
            'status': 'Winner'  # Assuming the status to be 'Winner', you can modify accordingly
        }
        
        # Call save_winner to save this data to the database
        save_winner(winner_data)

        # Create inline keyboard buttons
        markup = InlineKeyboardMarkup()
        createathon_button = InlineKeyboardButton("Go to Createathon", url="https://persistventures.com/createathon")
        get_hired_button = InlineKeyboardButton("Get Hired", url="https://get-a-job.persistventures.com/")
        
        # Add buttons to markup
        markup.add(createathon_button, get_hired_button)
        
        # Send congratulatory message with buttons
        bot.send_message(user_id, "Congratulations on completing the Challenge! You will receive your certificate shortly via email.", reply_markup=markup)
    else:
        # Show progress bar or percentage
        total_days = get_total_days_for_challenge(challenge_id)
        completed_days = get_completed_days_for_user(challenge_id, user_id)
        
        progress = (completed_days / total_days) * 100
        bot.send_message(user_id, f"Progress: {progress}%\nComplete the remaining tasks to finish.")

# Handle progress upload
@bot.callback_query_handler(func=lambda call: call.data.startswith("upload_"))
def upload_progress(call):
    _, challenge_id, day = call.data.split("_")

    # Check if the progress for this challenge and day already exists
    existing_progress = check_if_task_completed(challenge_id, day, call.message.chat.id)
    
    if existing_progress:
        # If progress already exists, notify the user and stop further action
        bot.send_message(call.message.chat.id, f"You've already completed this task for Challenge ID {challenge_id} on Day {day}. Please move to the next one!")
        return

    # If no existing progress, proceed with asking for progress description
    bot.send_message(call.message.chat.id, f"Please tell us about your progress for {day} of Challenge ID {challenge_id} in short.")
    
    # Register the state for capturing the progress description
    bot.register_next_step_handler(call.message, process_progress_description, challenge_id, day)

def process_progress_description(message, challenge_id, day):
    progress_text = message.text  # Get the progress description from the user
    
    # Prompt the user for the URL link
    bot.send_message(message.chat.id, "Now, please share the URL link for your progress.")
    
    # Register the state to capture the URL link
    bot.register_next_step_handler(message, save_progress_data, challenge_id, day, progress_text)

def save_progress_data(message, challenge_id, day, progress_text):
    progress_link = message.text  # Get the URL link from the user
    
    # Collect the data in a dictionary format to pass to the upload function
    progresstrack_data = {
        'user_id': message.chat.id,
        'challenge_id': challenge_id,
        'submit': True,  # Assuming the task is being uploaded
        'day': day,
        'link': progress_link,
        'challenge_day_id': f"{challenge_id}_{day}",  # Creating a unique challenge-day ID
        'text': progress_text
    }
    
    # Call the function to save progress data to the database
    upload_task_progress(progresstrack_data)
    
    # Notify the user that the progress has been uploaded
    bot.send_message(message.chat.id, f"Your progress for Challenge ID {challenge_id} on Day {day} has been uploaded successfully!")

    # Check if all tasks are completed for this challenge
    all_tasks_completed = check_all_tasks_completed(challenge_id, message.chat.id)
    
    if all_tasks_completed:
        # Send congratulatory message and buttons
        congrats_message = "Congratulations on completing the Challenge! You will receive your certificate shortly via email."
        
        # Create inline keyboard buttons
        markup = InlineKeyboardMarkup()
        createathon_button = InlineKeyboardButton("Go to Createathon", url="https://persistventures.com/createathon")
        get_hired_button = InlineKeyboardButton("Get Hired", url="https://get-a-job.persistventures.com/")
        
        # Add buttons to markup
        markup.add(createathon_button, get_hired_button)
        
        # Send the congratulatory message along with buttons
        bot.send_message(message.chat.id, congrats_message, reply_markup=markup)

# Function to check if all tasks are completed (you need to define this based on your database)
def check_all_tasks_completed(challenge_id, user_id):
    # Get the total days and timestamp for the challenge
    total_days = get_total_days_for_challenge(challenge_id)
    
    # Get the number of completed days for the user
    completed_days = get_completed_days_for_user(challenge_id, user_id)
    
    # Check if the total days equals the number of completed days
    return total_days == completed_days


# Start polling to receive messages
if __name__ == "__main__":
    bot.infinity_polling()