from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "List Sportmonks betting markets"

    def handle(self, *args, **options):
        service = SportmonksService()

        self.stdout.write("Loading Sportmonks markets...")

        try:
            result = service.get_markets()
            markets = result.get("data", [])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Markets returned: {len(markets)}"
                )
            )

            for market in markets:
                market_id = market.get("id")
                name = market.get("name")
                developer_name = market.get("developer_name")

                self.stdout.write(
                    f"Market ID: {market_id} | "
                    f"Name: {name} | "
                    f"Developer name: {developer_name}"
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks markets error: {e}"
                )
            )
