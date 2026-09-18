from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.text import slugify

from sports.models import Sport, League, Match
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Import today's fixtures from Sportmonks"

    def handle(self, *args, **options):
        service = SportmonksService()
        result = service.get_fixtures()
        fixtures = result.get("data", [])

        self.stdout.write(f"Sportmonks fixtures found: {len(fixtures)}")

        sport, _ = Sport.objects.get_or_create(
            slug="football",
            defaults={
                "name": "Football",
                "is_active": True,
            },
        )

        imported = 0

        for fixture in fixtures:
            fixture_id = fixture.get("id")
            name = fixture.get("name", "")
            starting_at = fixture.get("starting_at")

            if not fixture_id or not starting_at:
                continue

            # Teams
            participants = fixture.get("participants", [])

            home_team = None
            away_team = None

            for participant in participants:
                meta = participant.get("meta", {})
                location = meta.get("location")

                if location == "home":
                    home_team = participant.get("name")
                elif location == "away":
                    away_team = participant.get("name")

            # Fallback if participants are not available
            if not home_team or not away_team:
                if " vs " in name:
                    teams = name.split(" vs ", 1)
                    home_team = home_team or teams[0]
                    away_team = away_team or teams[1]

            if not home_team or not away_team:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping fixture {fixture_id}: teams not found"
                    )
                )
                continue

            # League
            league_data = fixture.get("league") or {}
            league_id = league_data.get("id")
            league_name = league_data.get("name") or "Unknown League"

            league_slug = slugify(
                f"sportmonks-{league_id or league_name}"
            )

            league, _ = League.objects.get_or_create(
                slug=league_slug,
                defaults={
                    "name": league_name,
                    "sport": sport,
                    "country_code": "XX",
                    "is_active": True,
                    "is_popular": True,
                    "source_url": (
                        f"sportmonks:league:{league_id}"
                        if league_id
                        else f"sportmonks:league:{league_slug}"
                    ),
                },
            )

                        # Match
            start_time = parse_datetime(starting_at)

            if start_time and timezone.is_naive(start_time):
                start_time = timezone.make_aware(
                    start_time,
                    timezone.get_current_timezone()
                )

            match, created = Match.objects.update_or_create(
                source_id=str(fixture_id),
                defaults={
                    "league": league,
                    "home_team": home_team,
                    "away_team": away_team,
                    "start_time": start_time,
                    "status": "scheduled",
                    "is_active": True,
                    "is_popular": False,
                    "is_bet_available": True,
                    "source_url": f"sportmonks:fixture:{fixture_id}",
                },
            )

            if created:
                imported += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Imported: {home_team} vs {away_team}"
                    )
                )
            else:
                self.stdout.write(
                    f"Updated: {home_team} vs {away_team}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished. New matches imported: {imported}"
            )
        )
