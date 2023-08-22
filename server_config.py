import os
import requests
from dotenv import load_dotenv

load_dotenv()

DeepFinder_api_url = os.getenv("API_URL")
DeepFinder_key = os.getenv("AUTH_KEY")

def get_server_config():
    try:
        params = {"key": DeepFinder_key}
        response = requests.get(DeepFinder_api_url, params={"key": DeepFinder_key}, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to get server config. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error while calling the API: {e}")
        return None
