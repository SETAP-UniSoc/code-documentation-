Admin Analytics
===============

Overview
--------

Provides analytical insights for society administrators.

Features
--------

- Membership growth tracking
- Event attendance statistics
- Most popular event
- Live member count

Endpoint
--------

.. code-block:: python

   path("my-analytics/", AnalyticsView.as_view(), name="analytics")

Authentication
--------------

- Required (Admin only)

Parameters
----------

- week
- month
- 6months
- year

Implementation
--------------

.. code-block:: python

   class AnalyticsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "admin":
            return Response({"error": "Admins only"}, status=403)

        period = request.query_params.get("period", "week")

        try:
            society = Society.objects.get(admin=request.user)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        now = timezone.now()

        # Decide grouping & range
        if period == "week":
            days_range = 7
            delta = timedelta(days=1)
            label_format = "%a"  # Mon Tue Wed
        elif period == "month":
            days_range = 30
            delta = timedelta(days=1)
            label_format = "%d %b"
        elif period == "6months":
            days_range = 26
            delta = timedelta(weeks=1)
            label_format = "Week %W"
        elif period == "year":
            days_range = 12
            delta = timedelta(days=30)
            label_format = "%b"
        else:
            return Response({"error": "Invalid period"}, status=400)

        start_date = now - (delta * days_range)

        labels = []
        totals = []

        current_date = start_date

        for _ in range(days_range):

            total = Membership.objects.filter(
                society=society,
                joined_at__lte=current_date
            ).filter(
                Q(left_at__isnull=True) | Q(left_at__gt=current_date)
            ).count()

            labels.append(current_date.strftime(label_format))
            totals.append(total)

            current_date += delta

        society = Society.objects.get(admin=request.user) # gets admis society
        total_events = society.events.count() # total events in that society
        events_stats = society.events.annotate(
            attendee_count = Count(
                "eventattendance",
                filter = Q(eventattendance__left_at__isnull=True)
            )
        ).values("title", "attendee_count")

        #most popular event
        most_popular = society.events.annotate(
            attendee_count = Count(
                "eventattendance",
                filter = Q(eventattendance__left_at__isnull=True)
            )
        ).order_by("-attendee_count").values("title", "attendee_count").first()

        live_count = Membership.objects.filter(
            society=society,
            left_at__isnull=True
        ).count()

        return Response({
            "labels": labels,
            "totals": totals,
            "live_count": live_count,
            "total_events": total_events,
            "events_stats": list(events_stats),
            "most_popular": most_popular,
            "event_attendance": list(events_stats)
        })

API view to provide analytics for a society admin.
Includes:
    - Membership growth over time
    - Total active members
    - Total events
    - Event attendance statistics
    - Most popular event

Query Parameters:
    - period: 'week', 'month', '6months', 'year'
