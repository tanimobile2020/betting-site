from django.core.management.base import BaseCommand
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "List unique Sportmonks markets from fixture odds"

    def handle(self, *args, **options):
        service = SportmonksService()

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

            markets = {}

            for odd in odds:
                market_id = odd.get("market_id")
                description = odd.get("market_description")

                if market_id not in markets:
                    markets[market_id] = {
                        "description": description,
                        "labels": set(),
                    }

                label = odd.get("label")

                if label:
                    markets[market_id]["labels"].add(
                        str(label)
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Unique markets found: {len(markets)}"
                )
            )

            for market_id in sorted(
                markets,
                key=lambda x: int(x)
            ):
                market = markets[market_id]

                labels = ", ".join(
                    sorted(market["labels"])
                )

                self.stdout.write(
                    f"Market ID: {market_id} | "
                    f"Description: {market['description']} | "
                    f"Labels: {labels}"
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks odds error: {e}"
                )
            )
