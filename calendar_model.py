import math
from typing import List, Tuple


class Day:
    def __init__(self, persian: Tuple[int, int, int], gregorian: Tuple[int, int, int], islamic: Tuple[int, int, int], is_holiday: bool, week_day: int,
                 week_num: int):
        self.persian = persian
        self.gregorian = gregorian
        self.islamic = islamic
        self.is_holiday = is_holiday
        self.week_day = week_day
        self.week_num = week_num

    def __str__(self):
        return f"persian={self.persian} - gregorian={self.gregorian} - islamic={self.islamic} - weekday={self.week_day}"

    def __repr__(self):
        return self.__str__()


PERSIAN_EPOCH = 1948320.5
GREGORIAN_EPOCH = 1721425.5
ISLAMIC_EPOCH = 1948439.5

PERSIAN_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
GREGORIAN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ISLAMIC_MONTHS = ["محرم", "صفر", "ربیع الاول", "ربیع الثاني", "جمادي الاول", "جمادي الثاني", "رجب", "شعبان", "رمضان", "شوال", "ذوالقعده", "ذوالحجه"]
WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]


def persian_to_jd(persian: Tuple[int, int, int]) -> float:
    year, month, day = persian
    epbase = year - (474 if year >= 0 else 473)
    epyear = 474 + epbase % 2820

    return (day +
            (((month - 1) * 31) if (month <= 7) else ((month - 1) * 30 + 6)) +
            math.floor((epyear * 682 - 110) / 2816) +
            (epyear - 1) * 365 +
            math.floor(epbase / 2820) * 1029983 +
            (PERSIAN_EPOCH - 1))


def jd_to_persian(jd: float) -> Tuple[int, int, int]:
    jd = math.floor(jd) + 0.5
    depoch = jd - persian_to_jd((475, 1, 1))
    cycle = math.floor(depoch / 1029983)
    cyear = depoch % 1029983
    if cyear == 1029982:
        ycycle = 2820
    else:
        aux1 = math.floor(cyear / 366)
        aux2 = cyear % 366
        ycycle = math.floor((2134 * aux1 + 2816 * aux2 + 2815) / 1028522) + aux1 + 1
    year = ycycle + 2820 * cycle + 474
    if year <= 0:
        year -= 1
    yday = jd - persian_to_jd((year, 1, 1)) + 1
    month = math.ceil(yday / 31) if yday <= 186 else math.ceil((yday - 6) / 30)
    day = jd - persian_to_jd((year, month, 1)) + 1

    return year, month, int(day)


def leap_persian(year: int) -> bool:
    return ((((year - (474 if year > 0 else 473)) % 2820) + 474 + 38) * 682) % 2816 < 682


def gregorian_to_jd(gregorian: Tuple[int, int, int]) -> float:
    year, month, day = gregorian
    return (GREGORIAN_EPOCH - 1 +
            365 * (year - 1) +
            math.floor((year - 1) / 4) -
            math.floor((year - 1) / 100) +
            math.floor((year - 1) / 400) +
            math.floor(
                (367 * month - 362) / 12 +
                (0 if month <= 2 else (-1 if leap_gregorian(year) else -2)) +
                day
            ))


def jd_to_gregorian(jd: float) -> Tuple[int, int, int]:
    wjd = math.floor(jd - 0.5) + 0.5
    depoch = wjd - GREGORIAN_EPOCH
    quadricent = math.floor(depoch / 146097)
    dqc = depoch % 146097
    cent = math.floor(dqc / 36524)
    dcent = dqc % 36524
    quad = math.floor(dcent / 1461)
    dquad = dcent % 1461
    yindex = math.floor(dquad / 365)
    year = quadricent * 400 + cent * 100 + quad * 4 + yindex
    if not (cent == 4 or yindex == 4):
        year += 1
    yearday = wjd - gregorian_to_jd((year, 1, 1))
    leapadj = 0 if wjd < gregorian_to_jd((year, 3, 1)) else (1 if leap_gregorian(year) else 2)
    month = math.floor(((yearday + leapadj) * 12 + 373) / 367)
    day = wjd - gregorian_to_jd((year, month, 1)) + 1

    return year, month, int(day)


def leap_gregorian(year: int) -> bool:
    return year % 4 == 0 and not (year % 100 == 0 and year % 400 != 0)


def islamic_to_jd(islamic: Tuple[int, int, int]) -> float:
    year, month, day = islamic

    return (day +
            math.ceil(29.5 * (month - 1)) +
            (year - 1) * 354 +
            math.floor((3 + 11 * year) / 30) +
            ISLAMIC_EPOCH - 1)


def jd_to_islamic(jd: float) -> Tuple[int, int, int]:
    jd = math.floor(jd) + 0.5
    year = math.floor((30 * (jd - ISLAMIC_EPOCH) + 10646) / 10631)
    month = min([
        12,
        math.ceil((jd - (29 + islamic_to_jd((year, 1, 1)))) / 29.5) + 1
    ])
    day = jd - islamic_to_jd((year, month, 1)) + 1
    return year, month, int(day)


def leap_islamic(year: int) -> bool:
    return (year * 11 + 14) % 30 < 11


def persian_to_gregorian(persian: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return jd_to_gregorian(persian_to_jd(persian))


def persian_to_islamic(persian: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return jd_to_islamic(persian_to_jd(persian))

    # 0 = Saturday


def weekday(jd: float) -> int:
    return (int(jd + 1.5) + 1) % 7


def get_day_from_persian(persian: Tuple[int, int, int], week_num: int):
    return Day(
        persian,
        persian_to_gregorian(persian),
        persian_to_islamic(persian),
        False,
        weekday(persian_to_jd(persian)),
        week_num
    )


def generate_days(persian_year: int) -> List[Day]:
    days = []
    week_num = 1
    persian_day = (persian_year, 1, 1)
    day = get_day_from_persian(persian_day, week_num)

    while True:
        if day.persian[0] == persian_year + 1:
            break

        days.append(day)

        year, month, day = persian_day

        if weekday(persian_to_jd(persian_day)) == 6:
            week_num += 1

        if month <= 6 and day == 31 or 7 <= month <= 11 and day == 30:
            day = 1
            month += 1
            week_num = 1
        elif month == 12 and (leap_persian(year) and day == 30 or not leap_persian(year) and day == 29):
            day = 1
            month = 1
            year += 1
            week_num = 1
        else:
            day += 1
        persian_day = (year, month, day)

        day = get_day_from_persian(persian_day, week_num)

    return days
