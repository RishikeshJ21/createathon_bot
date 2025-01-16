import requests
from bot.config import FB_ACCESS_TOKEN, GRAPH_API_URL

def fetch_instagram_data(instagram_username):
    url = f"{GRAPH_API_URL}/{instagram_username}?fields=username,followers_count,follows_count&access_token={FB_ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        raise Exception(data["error"]["message"])
    return {
        "username": data.get("username"),
        "followers": data.get("followers_count"),
        "following": data.get("follows_count"),
    }
