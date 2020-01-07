import datetime

from django.conf import settings as s
from rest_framework.response import Response
from rest_framework.views import APIView

from scidash.sciunittests.models import ScoreInstance


class DateRangeView(APIView):
    def get(self, request, *args, **kwargs):
        """Returns the initial search period (acceptable_period).
        for the first N (settings.ACCEPTABLE_SCORE_INSTANCES_AMOUNT) scores.

        Parameters
        ----------
        -

        Returns
        -------
        JSON object
        {
            "current_date": "<yyyy-mm-ddThh:mi:ss>",
            "acceptable_period": "<yyyy-mm-ddThh:mi:ss>"
        }
        """
        current_date = datetime.date.today() + datetime.timedelta(days=1)
        current_date_iso = datetime.datetime(
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )

        scores = ScoreInstance.objects.filter(
            timestamp__lt=current_date_iso).order_by('-timestamp')[
                 :s.ACCEPTABLE_SCORE_INSTANCES_AMOUNT]
        if scores:
            # found scores, acceptable period is scores last.timestamp
            # because sorting is DESC timestamp
            acceptable_period = scores.reverse()[0].timestamp
        else:
            # acceptable period defaults to current date - 1 year
            acceptable_period = datetime.datetime(
                year=current_date.year - 1,
                month=current_date.month,
                day=current_date.day
            )

        return Response(
            {
                "current_date": current_date_iso,
                "acceptable_period": acceptable_period
            }
        )
