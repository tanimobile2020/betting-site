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

            found = 0

            for odd in odds:
                label = str(odd.get("label", "")).strip().lower()

                if odd.get("market

            self.stdout.write(
                self.style.SUCCESS(
                    f"1X2 candidates found: {found}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
