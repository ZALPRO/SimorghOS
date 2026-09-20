#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سیمرغ‌اواس — موتور تقویم جلالی
==============================
پورت دقیق و راستی‌آزمایی‌شدهٔ الگوریتم مرجع jalaali-js
(https://github.com/jalaali/jalaali-js — مجوز MIT) به پایتون خالص،
به‌علاوهٔ لایهٔ نام‌ها و ارقام فارسی برای استفاده در waybar، hyprlock،
fastfetch و اپ خوش‌آمد سیمرغ.

    >>> from jalaali import to_jalaali
    >>> to_jalaali(2026, 9, 19)
    (1405, 6, 28)

مجوزِ این فایل (همراه سیمرغ‌اواس): GPL-3.0؛ بخش الگوریتم بر پایهٔ MIT جالاالی.
"""

from __future__ import annotations

FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"

MONTH_NAMES = (
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
)

WEEKDAY_NAMES = (  # اندیس = datetime.weekday() (دوشنبه=۰)
    "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه",
)

BREAKS = (
    -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181,
    1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178,
)
MIN_JALAALI_YEAR = BREAKS[0]
MAX_JALAALI_YEAR = BREAKS[-1] - 1


def div(a: int, b: int) -> int:
    """تقسیم صحیح با گِردکردن به صفر (معادل Math.trunc)."""
    q = a // b
    if (a % b != 0) and ((a < 0) != (b < 0)):
        q += 1
    return q


def mod(a: int, b: int) -> int:
    return a - div(a, b) * b


def fa_digits(value) -> str:
    """تبدیل ارقام لاتین به فارسی."""
    return "".join(FA_DIGITS[int(c)] if c.isdigit() else c for c in str(value))


def _leap_from_cycle(jump: int, n: int) -> int:
    """سال‌های سپری‌شده از آخرین سال کبیسه (۰ یعنی امسال کبیسه)."""
    adjusted = n
    if jump - n < 6:
        adjusted = n - jump + div(jump + 4, 33) * 33
    leap = mod(mod(adjusted + 1, 33) - 1, 4)
    if leap == -1:
        leap = 4
    return leap


def jal_cal_core(jy: int) -> dict:
    """پارامترهای سال جلالی: gy، march (روز مارسِ یکم فروردین)، leap."""
    if not (MIN_JALAALI_YEAR <= jy <= MAX_JALAALI_YEAR):
        raise ValueError(f"سال جلالی {jy} خارج از بازهٔ پشتیبانی است")
    gy = jy + 621
    leap_j = -14
    jp = BREAKS[0]
    jm = 0
    jump = 0
    for i in range(1, len(BREAKS)):
        jm = BREAKS[i]
        jump = jm - jp
        if jy < jm:
            break
        leap_j = leap_j + div(jump, 33) * 8 + div(mod(jump, 33), 4)
        jp = jm
    n = jy - jp
    leap_j = leap_j + div(n, 33) * 8 + div(mod(n, 33) + 3, 4)
    if mod(jump, 33) == 4 and jump - n == 4:
        leap_j += 1
    leap_g = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150
    march = 20 + leap_j - leap_g
    leap = _leap_from_cycle(jump, n)
    return {"gy": gy, "march": march, "leap": leap, "jump": jump, "n": n}


def g2d(gy: int, gm: int, gd: int) -> int:
    d = div((gy + div(gm - 8, 6) + 100100) * 1461, 4) \
        + div(153 * mod(gm + 9, 12) + 2, 5) \
        + gd - 34840408
    d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752
    return d


def d2g(jdn: int) -> tuple:
    j = 4 * jdn + 139361631
    j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
    i = div(mod(j, 1461), 4) * 5 + 308
    gd = div(mod(i, 153), 5) + 1
    gm = mod(div(i, 153), 12) + 1
    gy = div(j, 1461) - 100100 + div(8 - gm, 6)
    return gy, gm, gd


def j2d(jy: int, jm: int, jd: int) -> int:
    r = jal_cal_core(jy)
    return (g2d(r["gy"], 3, r["march"]) + (jm - 1) * 31
            - div(jm, 7) * (jm - 7) + jd - 1)


def d2j(jdn: int) -> tuple:
    gy, _gm, _gd = d2g(jdn)
    jy = min(gy - 621, MAX_JALAALI_YEAR)
    r = jal_cal_core(jy)
    jdn1f = g2d(r["gy"], 3, r["march"])
    k = jdn - jdn1f
    if k >= 0:
        if k <= 185:
            return jy, 1 + div(k, 31), mod(k, 31) + 1
        k -= 186
    else:
        jy -= 1
        k += 179
        if r["leap"] == 1:
            k += 1
    return jy, 7 + div(k, 30), mod(k, 30) + 1


def to_jalaali(gy: int, gm: int, gd: int) -> tuple:
    """میلادی → جلالی."""
    return d2j(g2d(gy, gm, gd))


def to_gregorian(jy: int, jm: int, jd: int) -> tuple:
    """جلالی → میلادی."""
    return d2g(j2d(jy, jm, jd))


def is_jalaali_leap(jy: int) -> bool:
    return jal_cal_core(jy)["leap"] == 0


def jalaali_month_length(jy: int, jm: int) -> int:
    if jm <= 6:
        return 31
    if jm <= 11:
        return 30
    return 30 if is_jalaali_leap(jy) else 29


def jalaali_month_name(jm: int) -> str:
    return MONTH_NAMES[jm - 1]


def jalaali_weekday_name(gy: int, gm: int, gd: int) -> str:
    """نام روز هفتهٔ فارسی برای یک تاریخ میلادی."""
    import datetime
    return WEEKDAY_NAMES[datetime.date(gy, gm, gd).weekday()]


if __name__ == "__main__":
    import datetime
    n = datetime.date.today()
    jy, jm, jd = to_jalaali(n.year, n.month, n.day)
    print(f"{jalaali_weekday_name(n.year, n.month, n.day)} {fa_digits(jd)} "
          f"{jalaali_month_name(jm)} {fa_digits(jy)}")
