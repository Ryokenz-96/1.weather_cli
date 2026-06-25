from datetime import datetime, timedelta,timezone
def get_local_time(utc_unixtime,offset_sec):
    utc_time=datetime.fromtimestamp(utc_unixtime,tz=timezone.utc)
    local_tz=timezone(timedelta(seconds=offset_sec))
    return utc_time.astimezone(local_tz)
    return datetime.fromtimestamp(utc_unixtime,tz=local_tz)
#alternate way for returning 