import os
import requests


class SportmonksService:
    BASE_URL = "https://api.sportmonks.com/v3/football"

    def __init__(self):
        self.token = os.environ.get("SPORTMONKS_API_TOKEN")

        if not self.token:
            raise ValueError("SPORTMONKS_API_TOKEN is not configured")

    def get_fixtures(self):
        url = f"{self.BASE_URL}/fixtures"

        response = requests.get(
            url,
            params={
                "api_token": self.token,
                "include": "participants;league;state",
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()
