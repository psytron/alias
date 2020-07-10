
from datetime import datetime, timezone,  timedelta

from datetime import timedelta

def series_now():
    #series = datetime.now().replace(second=0, microsecond=0)
    series = datetime.utcnow().replace(microsecond=0)
    return series

def series_now_minus( offset_in ):
    series = (datetime.utcnow() - timedelta(minutes=offset_in)  ).replace(microsecond=0)
    return series

def series( minutes_ago ):
    #timeago = datetime.now() - timedelta(minutes=minutes_ago) +  timedelta( hours=8) #why was this here
    #                                                            on server this should be gone
    timeago = datetime.utcnow() - timedelta(minutes=minutes_ago) #+  timedelta( hours=7)
    series = timeago.replace(second=0, microsecond=0)
    return series


def series_span( datetime_in , minutes_span ):
    #timeago = datetime.now() - timedelta(minutes=minutes_ago) +  timedelta( hours=8) #why was this here
    #                                                            on server this should be gone
    letime = datetime_in + timedelta( minutes=minutes_span ) #+  timedelta( hours=7)
    series = letime.replace( second=0, microsecond=0 )
    return series


def utc_stamp():
    sincex=int( datetime.utcnow().timestamp() ) * 1000
    return sincex