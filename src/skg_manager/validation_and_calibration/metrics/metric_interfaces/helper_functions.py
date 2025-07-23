from datetime import datetime


def check_is_date(timestamp):
    try:
        is_date = bool(datetime.strptime(timestamp, "%Y-%m-%d"))
    except ValueError:
        is_date = False
    return is_date


def check_datetime_is_correct_format(timestamp):
    try:
        is_date_time = bool(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        is_date_time = False
    return is_date_time

def check_start_and_end_times(start_time, end_time):
    if start_time is None:
        start_time = "1970-01-01 00:00:00"
    if end_time is None:
        end_time = "2970-01-01 23:59:59"

    if check_is_date(start_time):  # add hours et cetera
        start_time = f"{start_time} 00:00:00"
    if check_is_date(end_time):  # add hours et cetera
        end_time = f"{end_time} 23:59:59"

    if not check_datetime_is_correct_format(start_time):
        raise ValueError(
            f"start_time: {start_time} is of incorrect format, it should be %Y-%m-%d or %Y-%m-%d %H:%M:%S")

    if not check_datetime_is_correct_format(end_time):
        raise ValueError(
            f"start_time: {end_time} is of incorrect format, it should be %Y-%m-%d or %Y-%m-%d %H:%M:%S")

    return start_time, end_time

