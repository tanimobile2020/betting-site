from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Find Sportmonks 1X2 market"

    def handle(self, *args, **options):
        service = SportmonksService()
        fixture_id = 19722783

        self.stdout.write(
            f"Searching 1X2 odds for fixture {fixture_id}..."
        )

        try:
            result = service.get_fixture_odds(fixture_id)
            odds = result.get("data", [])

            self.stdout.write(
                f"Total odds returned: {len(odds)}"
            )

            groups = {}

            for odd in odds:
                market_id = odd.get("market_id")
                bookmaker_id = odd.get("bookmaker_id")
                label = str(odd.get("label", "")).strip().upper()

                key = (market_id, bookmaker_id)

                if key not in groups:
                    groups[key] = {}

                if label in ["1", "X", "2"]:
                    groups[key][label] = odd.get("value")

            found = 0

            for (market_id, bookmaker_id), selections in groups.items():
                if all(label in selections for label in ["1", "X", "2"]):
                    found += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"1X2 FOUND | "
                            f"Market: {market_id} | "
                            f"Bookmaker: {bookmaker_id} | "
                            f"1: {selections['1']} | "
                            f"X: {selections['X']} | "
                            f"2: {selections['2']}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Complete 1X2 groups found: {found}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
