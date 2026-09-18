from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Test Sportmonks odds"

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
                    f"Odds returned: {len(odds)}"
                )
            )

            for odd in odds[:30]:
                self.stdout.write(
                    f"Market: {odd.get('market_id')} | "
                    f"Bookmaker: {odd.get('bookmaker_id')} | "
                    f"Label: {odd.get('label')} | "
                    f"Value: {odd.get('value')}"
                )

            if not odds:
                self.stdout.write(
                    self.style.WARNING(
                        "No odds returned for this fixture."
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
