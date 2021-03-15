import datetime


def parse_scan_result(result: str) -> dict:
    return dict(map(lambda x: x.split("="), result.split("&")))


def filling_all(*fields):
    return all(fields)


def get_bounds_by_period(period):
    end_date = datetime.datetime.now()
    if period == "day":
        delta_date = datetime.timedelta(days=1)
    elif period == "week":
        delta_date = datetime.timedelta(weeks=1)
    elif period == "month":
        delta_date = datetime.timedelta(days=30)
    elif period == "year":
        delta_date = datetime.timedelta(days=365)
    else:
        return
    return end_date - delta_date, end_date


def get_datetime(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


def datetime_to_str(date_time: datetime.datetime):
    return date_time.strftime("%Y-%m-%dT%H:%M:%S")
