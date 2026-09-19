from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify

from sports.models import Sport, League, Match
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Import Sportmonks fixtures and 1X2 odds"

    MARKET_ID = 1
    BOOKMAKER_ID = 2

    def handle(self, *args, **options):
        service = SportmonksService()

        self.stdout.write("Loading Sportmonks fixtures...")

        try:
            result = service.get_fixtures()
            fixtures = result.get("data", [])
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks fixtures error: {e}"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Fixtures returned: {len(fixtures)}"
            )
        )

        sport, _ = Sport.objects.get_or_create(
            slug="football",
            defaults={
                "name": "Football",
                "is_active": True,
            },
        )

        for fixture in fixtures:
            try:
                self.import_fixture(
                    service,
                    sport,
                    fixture,
                )
            except Exception as e:
                fixture_id = fixture.get("id")

                self.stdout.write(
                    self.style.ERROR(
                        f"Fixture {fixture_id} error: {e}"
                    )
                )

    def import_fixture(self, service, sport, fixture):
        fixture_id = fixture.get("id")

        if not fixture_id:
            return

        league_data = fixture.get("league") or {}
        league_id = league_data.get("id")
        league_name = league_data.get("name") or "Sportmonks"

        league_slug = (
            f"sportmonks-{league_id}"
            if league_id
            else f"sportmonks-{slugify(league_name)}"
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
                    else None
                ),
            },
        )

        participants = fixture.get("participants") or []

        home_team = None
        away_team = None

        for participant in participants:
            meta = participant.get("meta") or {}
            location = meta.get("location")
            name = participant.get("name")

            if location == "home":
                home_team = name
            elif location == "away":
                away_team = name

        fixture_name = fixture.get("name") or ""

        if (
            (not home_team or not away_team)
            and " vs " in fixture_name
        ):
            parts = fixture_name.split(" vs ", 1)

            if not home_team:
                home_team = parts[0].strip()

            if not away_team:
                away_team = parts[1].strip()

        if not home_team:
            home_team = "Home"

        if not away_team:
            away_team = "Away"

        starting_at = fixture.get("starting_at")
        start_time = parse_datetime(starting_at)

        if start_time and timezone.is_naive(start_time):
            start_time = timezone.make_aware(
                start_time,
                timezone.get_current_timezone(),
            )

        if not start_time:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipping fixture {fixture_id}: "
                    f"no valid start time"
                )
            )
            return

        home_odds = None
        draw_odds = None
        away_odds = None

        try:
            odds_result = service.get_fixture_odds(
                fixture_id
            )

            odds = odds_result.get("data", [])

            for odd in odds:
                if odd.get("market_id") != self.MARKET_ID:
                    continue

                if (
                    odd.get("bookmaker_id")
                    != self.BOOKMAKER_ID
                ):
                    continue

                label = odd.get("label")
                value = odd.get("value")

                if value is None:
                    continue

                try:
                    value = Decimal(str(value))
                except InvalidOperation:
                    continue

                if label == "Home":
                    home_odds = value

                elif label == "Draw":
                    draw_odds = value

                elif label == "Away":
                    away_odds = value

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Odds error for fixture "
                    f"{fixture_id}: {e}"
                )
            )

        has_complete_odds = all(
            value is not None
            for value in (
                home_odds,
                draw_odds,
                away_odds,
            )
        )

        defaults = {
            "league": league,
            "home_team": home_team,
            "away_team": away_team,
            "start_time": start_time,
            "status": "scheduled",
            "is_active": True,
            "is_popular": False,
            "is_bet_available": has_complete_odds,
            "source_url": (
                f"sportmonks:fixture:{fixture_id}"
            ),
        }

        if has_complete_odds:
            defaults.update(
                {
                    "home_win_odds": home_odds,
                    "draw_odds": draw_odds,
                    "away_win_odds": away_odds,
                    "last_odds_update": timezone.now(),
                }
            )

        match, created = Match.objects.update_or_create(
            source_id=str(fixture_id),
            defaults=defaults,
        )

        action = "Created" if created else "Updated"

        if has_complete_odds:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: "
                    f"{home_team} vs {away_team} | "
                    f"1={home_odds} "
                    f"X={draw_odds} "
                    f"2={away_odds}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"{action}: "
                    f"{home_team} vs {away_team} | "
                    f"No complete 1X2 odds "
                    f"from bookmaker {self.BOOKMAKER_ID}"
                )
            )
