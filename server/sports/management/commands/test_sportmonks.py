from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Test Sportmonks 1X2 odds"

    def handle(self, *args, **options):
        service = SportmonksService()
        fixture_id = 19722783

        self.stdout.write(
            f"Testing Sportmonks odds for fixture {fixture_id}..."
        )

        try:
            result = service.get_fixture_odds(fixture_id)
            odds = result.get("data", [])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Total odds returned: {len(odds)}"
                )
            )

            found = 0

            for odd in odds:
                if odd.get("market_id") == 19:
                    self.stdout.write(
                        f"Market: {odd.get('market_id')} | "
                        f"Bookmaker: {odd.get('bookmaker_id')} | "
                        f"Label: {odd.get('label')} | "
                        f"Value: {odd.get('value')}"
                    )
                    found += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Market 19 odds found: {found}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
