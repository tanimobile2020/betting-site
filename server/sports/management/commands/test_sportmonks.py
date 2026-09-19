from collections import defaultdict

from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Show Fulltime Result odds grouped by bookmaker"

    def handle(self, *args, **options):
        service = SportmonksService()

        fixture_id = 19722783
        market_id = 1

        self.stdout.write(
            f"Loading Fulltime Result odds "
            f"for fixture {fixture_id}..."
        )

        try:
            result = service.get_fixture_odds(fixture_id)
            odds = result.get("data", [])

            bookmakers = defaultdict(dict)

            for odd in odds:
                if odd.get("market_id") != market_id:
                    continue

                bookmaker_id = odd.get("bookmaker_id")
                label = odd.get("label")
                value = odd.get("value")

                if label in ("Home", "Draw", "Away"):
                    bookmakers[bookmaker_id][label] = value

            self.stdout.write(
                self.style.SUCCESS(
                    f"Bookmakers found: {len(bookmakers)}"
                )
            )

            for bookmaker_id, values in sorted(
                bookmakers.items(),
                key=lambda item: int(item[0])
            ):
                home = values.get("Home", "-")
                draw = values.get("Draw", "-")
                away = values.get("Away", "-")

                complete = all(
                    label in values
                    for label in ("Home", "Draw", "Away")
                )

                status = "COMPLETE" if complete else "INCOMPLETE"

                self.stdout.write(
                    f"Bookmaker ID: {bookmaker_id} | "
                    f"Home: {home} | "
                    f"Draw: {draw} | "
                    f"Away: {away} | "
                    f"{status}"
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
