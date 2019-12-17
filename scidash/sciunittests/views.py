import datetime

from django.conf import settings as s
from rest_framework.response import Response
from rest_framework.views import APIView

from scidash.sciunittests.models import ScoreInstance


class DateRangeView(APIView):
    def get(self, request, *args, **kwargs):
        three_month_period = datetime.timedelta(3 * 365 / 12)
        current_date = datetime.date.today() + datetime.timedelta(days=1)
        current_date_iso = datetime.datetime(
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )

        acceptable_period = None

        for quarter in range(1, s.SCIDASH_INITIAL_SEARCH_QUARTERS + 1):
            period = current_date_iso - quarter*three_month_period
            count = ScoreInstance.objects.filter(
                timestamp__gte=period, timestamp__lt=current_date_iso
            ).count()

            if count > s.ACCEPTABLE_SCORE_INSTANCES_AMOUNT:
                acceptable_period = period
                break

        if acceptable_period is None:
            acceptable_period = period

        return Response(
            {
                "current_date": current_date_iso,
                "acceptable_period": acceptable_period
            }
        )
