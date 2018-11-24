import datetime

from django.shortcuts import render
from django.conf import settings as s
from rest_framework.views import APIView
from rest_framework.response import Response

from scidash.sciunittests.models import ScoreInstance


class DateRangeView(APIView):

    def get(self, request, *args, **kwargs):
        three_month_period = datetime.timedelta(3*365/12)
        current_date = datetime.date.today()
        current_date_iso = datetime.datetime(
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )

        three_month_ago = current_date_iso - three_month_period
        six_month_ago = three_month_ago - three_month_period
        nine_month_ago = six_month_ago - three_month_period

        acceptable_period = None

        for period in [three_month_ago, six_month_ago, nine_month_ago]:
            count = ScoreInstance.objects.filter(
                timestamp__gte=period,
                timestamp__lt=current_date_iso
            ).count()

            if count > s.ACCEPTABLE_SCORE_INSTANCES_AMOUNT:
                acceptable_period = period
                break

        return Response({
            "current_date": current_date_iso,
            "acceptable_period": acceptable_period
        })
