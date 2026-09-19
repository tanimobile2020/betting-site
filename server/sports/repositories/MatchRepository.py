from django.db.models import Q, OuterRef
from django.db.models.manager import BaseManager
from django.utils import timezone
from sports.models import Match


class MatchRepository:
    @staticmethod
    def get_upcoming_matches() -> BaseManager[Match]:
        """
        Get upcoming matches that are active.
        Matches are shown even if betting odds are not available yet.
        """
        now = timezone.now()

        return Match.objects.filter(
            league=OuterRef("pk"),
            is_active=True
        ).filter(
            Q(status="live") |
            Q(status="scheduled", start_time__gte=now)
        )

    @staticmethod
    def get_popular_matches() -> BaseManager[Match]:
        """
        Get all upcoming active matches for homepage.
        """
        now = timezone.now()

        return (
            Match.objects.filter(
                is_active=True
            )
            .filter(
                Q(status="live") |
                Q(status="scheduled", start_time__gte=now)
            )
            .order_by("-status", "start_time")[:15]
        )

    @staticmethod
    def get_league_matches(league: str) -> BaseManager[Match]:
        """
        Get matches for a specific league that are active.
        """
        now = timezone.now()

        return (
            Match.objects.filter(
                league=league,
                is_active=True
            )
            .filter(
                Q(status="live") |
                Q(status="scheduled", start_time__gte=now)
            )
            .order_by("-status", "start_time")
        )

    @staticmethod
    def get_active_match(match_id: int) -> Match:
        """
        Get a single active match by its ID.
        """
        return Match.objects.get(
            id=match_id,
            is_active=True
        )

    @staticmethod
    def get_matches_by_ids(match_ids: list[int]) -> BaseManager[Match]:
        """
        Get matches by their IDs.
        """
        return Match.objects.filter(
            id__in=match_ids
        )
