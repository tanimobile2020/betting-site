@staticmethod
def get_popular_matches() -> BaseManager[Match]:
    """
    Get upcoming active matches for homepage.
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
