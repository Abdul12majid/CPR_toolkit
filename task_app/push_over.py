import pytz
from datetime import datetime
import requests


la_timezone = pytz.timezone('America/Los_Angeles')
# Get current time in LA
la_time = datetime.now(la_timezone)

def belle_push_notis():
    group_key = "g938i4h5rne5se29hhgvkd85kzjfne"
    api_token = "ahp8xpq6pcobmpeye54kd9x3n6fmdi"
    formatted_time = la_time.strftime("%m/%d %H:%M")

    data = {
        "token": api_token,
        "user": group_key,
        "device": "",
        "sound": "bike",
        "priority": 0,
        "title": "Sinnamon Alert!",
        "message": f"New ToDO on your list, please check.", 
        "url": f"https://spleecho.pythonanywhere.com/",
        "url_title": "Go To Dashboard",
        "ttl": 7200,
    }

    notis_url = "https://api.pushover.net/1/messages.json"
    response = requests.post(notis_url, data=data)

    if response.status_code == 200:
        print("sent notification", flush=True)
    else:
        print("error")