from . import jalali
from django.utils import timezone


def persian_number_converter(string):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    for e, p in numbers.items():
        string = string.replace(e, p)
    return string


def jalali_converter(time):
    jmonths = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند",]
    time = timezone.localtime(time)
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    output = "{} {} {}, ساعت {}:{}".format(
        time_to_tuple[2],
        jmonths[time_to_tuple[1] - 1],
        time_to_tuple[0],
        time.hour,
        time.minute
    )
    return persian_number_converter(output)
