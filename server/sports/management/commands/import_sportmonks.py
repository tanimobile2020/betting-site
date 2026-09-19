from decimal import Decimal, InvalidOperation
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify

from sports.models import (
    Sport,
    League,
    Match,
    BetType,
    BetOption,
)
from sports.services.sportmonks import SportmonksService


class Command(BaseCommand):
    help = "Import Sportmonks fixtures and all available odds"

    BOOKMAKER_ID = 2
    MARKET_1X2_ID = 1
    DAYS_TO_IMPORT = 7

    def handle(self, *args, **options):
        service = SportmonksService()

        today = timezone.localdate()
        end_date = today + timedelta(
            days=self.DAYS_TO_IMPORT - 1
        )

        start_string = today.isoformat()
        end_string = end_date.isoformat()

        self.stdout.write(
            f"Loading Sportmonks fixtures "
            f"from {start_string} to {end_string}..."
        )

        # ---------------------------------------
        # LOAD FIXTURES FOR THE WHOLE DATE RANGE
        # ---------------------------------------

        try:
            result = service.get_fixtures_between(
                start_string,
                end_string,
            )

            all_fixtures = result.get("data", []) or []

            self.stdout.write(
                self.style.SUCCESS(
                    f"Total fixtures returned "
                    f"for {start_string} -> {end_string}: "
                    f"{len(all_fixtures)}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Sportmonks fixtures error: {e}"
                )
            )
            return

        # ---------------------------------------
        # SHOW NUMBER OF FIXTURES PER DAY
        # ---------------------------------------

        fixture_counts = {}

        for fixture in all_fixtures:
            starting_at = fixture.get("starting_at")

            if not starting_at:
                continue

            fixture_date = starting_at[:10]

            fixture_counts[fixture_date] = (
                fixture_counts.get(fixture_date, 0) + 1
            )

        for day_offset in range(self.DAYS_TO_IMPORT):
            current_date = today + timedelta(days=day_offset)
            date_string = current_date.isoformat()

            count = fixture_counts.get(date_string, 0)

            self.stdout.write(
                f"{date_string}: {count} fixtures returned"
            )

        # ---------------------------------------
        # SPORT
        # ---------------------------------------

        sport, _ = Sport.objects.get_or_create(
            slug="football",
            defaults={
                "name": "Football",
                "is_active": True,
            },
        )

        # ---------------------------------------
        # IMPORT FIXTURES
        # ---------------------------------------

        for fixture in all_fixtures:
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

    def import_fixture(
        self,
        service,
        sport,
        fixture,
    ):
        fixture_id = fixture.get("id")

        if not fixture_id:
            return

        # ---------------------------------------
        # LEAGUE
        # ---------------------------------------

        league_data = fixture.get("league") or {}

        league_id = league_data.get("id")

        league_name = (
            league_data.get("name")
            or "Sportmonks League"
        )

        if league_id:
            league_slug = f"sportmonks-{league_id}"
        else:
            league_slug = (
                f"sportmonks-{slugify(league_name)}"
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

        # ---------------------------------------
        # TEAMS
        # ---------------------------------------

        participants = (
            fixture.get("participants")
            or []
        )

        home_team = None
        away_team = None

        for participant in participants:
            meta = (
                participant.get("meta")
                or {}
            )

            location = meta.get("location")
            name = participant.get("name")

            if location == "home":
                home_team = name

            elif location == "away":
                away_team = name

        fixture_name = (
            fixture.get("name")
            or ""
        )

        if (
            (not home_team or not away_team)
            and " vs " in fixture_name
        ):
            parts = fixture_name.split(
                " vs ",
                1,
            )

            if not home_team:
                home_team = parts[0].strip()

            if not away_team:
                away_team = parts[1].strip()

        if not home_team:
            home_team = "Home"

        if not away_team:
            away_team = "Away"

        # ---------------------------------------
        # START TIME
        # ---------------------------------------

        starting_at = fixture.get("starting_at")

        start_time = parse_datetime(starting_at)

        if (
            start_time
            and timezone.is_naive(start_time)
        ):
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

        # ---------------------------------------
        # GET ALL ODDS
        # ---------------------------------------

        odds = []

        try:
            odds_result = service.get_fixture_odds(
                fixture_id
            )

            odds = (
                odds_result.get("data")
                or []
            )

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Odds error for fixture "
                    f"{fixture_id}: {e}"
                )
            )

        # ---------------------------------------
        # FIND 1X2
        # ---------------------------------------

        home_odds = None
        draw_odds = None
        away_odds = None

        for odd in odds:

            if (
                odd.get("market_id")
                != self.MARKET_1X2_ID
            ):
                continue

            if (
                odd.get("bookmaker_id")
                != self.BOOKMAKER_ID
            ):
                continue

            label = odd.get("label")
            value = odd.get("value")

            decimal_value = self.to_decimal(value)

            if decimal_value is None:
                continue

            normalized_label = (
                str(label)
                .strip()
                .lower()
            )

            if normalized_label in (
                "home",
                "1",
            ):
                home_odds = decimal_value

            elif normalized_label in (
                "draw",
                "x",
            ):
                draw_odds = decimal_value

            elif normalized_label in (
                "away",
                "2",
            ):
                away_odds = decimal_value

        has_complete_1x2 = all(
            value is not None
            for value in (
                home_odds,
                draw_odds,
                away_odds,
            )
        )

        # ---------------------------------------
        # CREATE / UPDATE MATCH
        # ---------------------------------------

        defaults = {
            "league": league,
            "home_team": home_team,
            "away_team": away_team,
            "start_time": start_time,
            "status": "scheduled",
            "is_active": True,
            "is_popular": True,
            "is_bet_available": len(odds) > 0,
            "source_url": (
                f"sportmonks:fixture:{fixture_id}"
            ),
        }

        if has_complete_1x2:
            defaults.update(
                {
                    "home_win_odds": home_odds,
                    "draw_odds": draw_odds,
                    "away_win_odds": away_odds,
                    "last_odds_update": timezone.now(),
                }
            )

        match, created = (
            Match.objects.update_or_create(
                source_id=str(fixture_id),
                defaults=defaults,
            )
        )

        # ---------------------------------------
        # IMPORT ALL MARKETS / ODDS
        # ---------------------------------------

        imported_options = self.import_all_odds(
            match,
            odds,
        )

        action = (
            "Created"
            if created
            else "Updated"
        )

        if has_complete_1x2:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: "
                    f"{home_team} vs {away_team} | "
                    f"1={home_odds} "
                    f"X={draw_odds} "
                    f"2={away_odds} | "
                    f"Bet options={imported_options}"
                )
            )

        else:
            self.stdout.write(
                self.style.WARNING(
                    f"{action}: "
                    f"{home_team} vs {away_team} | "
                    f"No complete 1X2 | "
                    f"Bet options={imported_options}"
                )
            )

    def import_all_odds(
        self,
        match,
        odds,
    ):
        imported = 0

        # Delete old imported odds for this match.
        BetOption.objects.filter(
            match=match
        ).delete()

        for odd in odds:

            bookmaker_id = odd.get(
                "bookmaker_id"
            )

            if (
                bookmaker_id
                != self.BOOKMAKER_ID
            ):
                continue

            market_id = odd.get(
                "market_id"
            )

            if market_id is None:
                continue

            label = odd.get("label")

            if label is None:
                continue

            raw_value = odd.get("value")

            decimal_value = self.to_decimal(
                raw_value
            )

            if decimal_value is None:
                continue

            # -----------------------------------
            # MARKET NAME
            # -----------------------------------

            market_name = (
                odd.get("market_name")
                or odd.get(
                    "market_description"
                )
                or f"Market {market_id}"
            )

            market_code = (
                f"sportmonks_{market_id}"
            )

            bet_type, _ = (
                BetType.objects.get_or_create(
                    code=market_code,
                    defaults={
                        "name": market_name,
                        "is_active": True,
                    },
                )
            )

            if (
                market_name
                and bet_type.name != market_name
                and not market_name.startswith(
                    "Market "
                )
            ):
                bet_type.name = market_name

                bet_type.save(
                    update_fields=[
                        "name"
                    ]
                )

            # -----------------------------------
            # OPTION LABEL
            # -----------------------------------

            option_label = str(
                label
            ).strip()

            total = odd.get("total")

            handicap = odd.get(
                "handicap"
            )

            if (
                total is not None
                and str(total)
                not in option_label
            ):
                option_label = (
                    f"{option_label} {total}"
                )

            if (
                handicap is not None
                and str(handicap)
                not in option_label
            ):
                option_label = (
                    f"{option_label} {handicap}"
                )

            option_label = option_label[:50]

            # -----------------------------------
            # SAVE BET OPTION
            # -----------------------------------

            BetOption.objects.create(
                match=match,
                bet_type=bet_type,
                value=option_label,
                odds=decimal_value,
            )

            imported += 1

        return imported

    def to_decimal(
        self,
        value,
    ):
        if value is None:
            return None

        try:
            decimal_value = Decimal(
                str(value)
            )

            return decimal_value.quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):
            return None
