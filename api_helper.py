import requests
import json

def send_to_api(content):
    url = "https://mysite-x067.onrender.com/rides/add_rides"
    headers = {"Content-Type": "application/json"}
    json_content = json.loads(content)
    try:
        response = requests.post(url, json=json_content, headers=headers, timeout=100)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return "Content successfully sent to the API!"
    except requests.exceptions.RequestException as e:
        # Log or print the error
        print(f"Error sending content to API: {e}")
        return f"Failed to send content: {e}"
