import pytz
import datetime

def to_utc_ms(date, tz = 'US/Eastern'):
    dt = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    dt = pytz.timezone(tz).localize(dt)
    return int(dt.timestamp() * 1000.0)
