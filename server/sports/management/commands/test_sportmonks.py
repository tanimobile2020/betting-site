import json

from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Inspect Sportmonks odds structure"

    def handle(self, *args, **options):
        service = SportmonksService()

        # Fixture që e dimë se ka odds
        fixture_id = 19722783

        self.stdout.write(
            f"Loading odds for fixture {fixture_id}..."
        )

        try:
            result = service.get_fixture_odds(fixture_id)
            odds = result.get("data", [])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Total odds returned: {len(odds)}"
                )
            )

            if not odds:
                self.stdout.write(
                    self.style.WARNING("No odds returned.")
                )
                return

            # Printojmë vetëm 10 rekordet e para,
            # por me TË GJITHA fushat që kthen API-ja.
            for index, odd in enumerate(odds[:10], start=1):
                self.stdout.write(
                    f"\n========== ODD {index} =========="
                )

                self.stdout.write(
                    json.dumps(
                        odd,
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
