import os
from datetime import date as date_class

import requests


class SportmonksService:
    BASE_URL = "https://api.sportmonks.com/v3/football"

    def __init__(self):
        self.token = os.environ.get("SPORTMONKS_API_TOKEN")

        if not self.token:
            raise ValueError(
                "SPORTMONKS_API_TOKEN is not configured"
            )

    def get_fixtures(self, date=None):
        """
        Get fixtures for a specific date.
        """
        if date is None:
            date = date_class.today().isoformat()

        url = f"{self.BASE_URL}/fixtures/date/{date}"

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

    def get_fixtures_between(self, start_date, end_date):
        """
        Get fixtures between two dates.
        Used to test/fetch multiple future days in one request.
        """
        url = (
            f"{self.BASE_URL}/fixtures/between/"
            f"{start_date}/{end_date}"
        )

        response = requests.get(
            url,
            params={
                "api_token": self.token,
                "include": "participants;league;state",
                "per_page": 100,
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_fixture_odds(self, fixture_id):
        url = (
            f"{self.BASE_URL}/odds/pre-match/"
            f"fixtures/{fixture_id}"
        )

        response = requests.get(
            url,
            params={
                "api_token": self.token,
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_markets(self):
        url = f"{self.BASE_URL}/markets"

        response = requests.get(
            url,
            params={
                "api_token": self.token,
                "per_page": 100,
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()
