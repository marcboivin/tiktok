import datetime
from durations import total_seconds

utc_datetime = '%Y-%m-%dT%H:%M:%SZ'

def parse_isoutc( text ):

    dt = datetime.datetime.strptime( text, utc_datetime )
    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
    secs = total_seconds( dt - epoch )
    return datetime.datetime.fromtimestamp( secs )

