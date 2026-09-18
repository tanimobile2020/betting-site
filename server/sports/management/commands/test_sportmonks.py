from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Test Sportmonks API connection"

    def handle(self, *args, **options):
        self.stdout.write("Connecting to Sportmonks...")

        try:
            service = SportmonksService()
            result = service.get_fixtures()

            fixtures = result.get("data", [])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Sportmonks connection OK. Fixtures returned: {len(fixtures)}"
                )
            )

            for fixture in fixtures[:10]:
                fixture_id = fixture.get("id")
                name = fixture.get("name")
                starting_at = fixture.get("starting_at")

                self.stdout.write(
                    f"ID: {fixture_id} | {name} | {starting_at}"
                )

            if not fixtures:
                self.stdout.write(
                    self.style.WARNING(
                        "Connection works, but this endpoint returned no fixtures."
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Sportmonks error: {e}")
            )
