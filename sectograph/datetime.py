import typing
from datetime import date, datetime, time, timedelta


# this module is useful to set exact date/time for a whole app.
# instead of using current date/time we cat set here any date/time we want.
# so, in future there will be possible to implement "time travel".
# it is also re-exports all `datetime` classes, so it is save to use
# this module instead of regular `datetime`.


_date: typing.Optional[date] = None
_time: typing.Optional[time] = None


def app_now() -> datetime:
    if _date is None and _time is None:
        return datetime.now()
    if _date is None:
        return datetime.combine(date.today(), _time)
    if _time is None:
        return datetime.combine(_date, time())
    return datetime.combine(_date, _time)


def app_today() -> date:
    if _date is None:
        return date.today()
    return _date


def app_time() -> time:
    if _time is None:
        return time()
    return _time


def set_app_datetime(
    *, time: time = None, date: date = None, datetime: datetime = None
) -> None:
    global _date, _time
    if time is not None:
        _time = time
    if date is not None:
        _date = date
    if datetime is not None:
        _date = datetime.date()
        _time = datetime.time()


def reset_app_datetime() -> None:
    global _date, _time
    _date = None
    _time = None


# set_app_datetime(
#     date=date(year=2021, month=3, day=7),
#     time=time(hour=10, minute=11, second=3),
# )
