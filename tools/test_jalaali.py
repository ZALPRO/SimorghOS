#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""آزمون‌های موتور جلالی سیمرغ‌اواس — راستی‌آزمایی با jcal (libjalali)."""
import datetime
import shutil
import subprocess
import sys
import unittest

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from jalaali import (  # noqa: E402
    to_jalaali, to_gregorian, fa_digits, jalaali_month_name,
    jalaali_weekday_name, is_jalaali_leap,
)

KNOWN = [
    # (gregorian, jalaali)
    ((2026, 9, 19), (1405, 6, 28)),   # امروز: شنبه ۲۸ شهریور ۱۴۰۵
    ((2026, 3, 21), (1405, 1, 1)),    # نوروز ۱۴۰۵
    ((2025, 3, 21), (1404, 1, 1)),    # نوروز ۱۴۰۴
    ((2024, 3, 20), (1403, 1, 1)),    # سال کبیسه میلادی
    ((1979, 2, 11), (1357, 11, 22)),  # پیروزی انقلاب
    ((2000, 1, 1), (1378, 10, 11)),
    ((2026, 12, 31), (1405, 10, 10)),
]


class TestJalaali(unittest.TestCase):
    def test_known_dates(self):
        for (gy, gm, gd), (jy, jm, jd) in KNOWN:
            self.assertEqual(to_jalaali(gy, gm, gd), (jy, jm, jd),
                             f"{gy}-{gm}-{gd}")

    def test_roundtrip(self):
        d = datetime.date(2020, 1, 1)
        for _ in range(365 * 8):  # هشت سال رفت‌وبرگشت
            jy, jm, jd = to_jalaali(d.year, d.month, d.day)
            self.assertEqual(to_gregorian(jy, jm, jd), (d.year, d.month, d.day))
            d += datetime.timedelta(days=1)

    def test_cross_check_jcal(self):
        """مقایسه با کتابخانه رسمی libjalali (ابزار jdate) اگر نصب باشد."""
        if not shutil.which("jdate"):
            self.skipTest("jdate نصب نیست")
        import random
        random.seed(7)
        for _ in range(60):
            d = datetime.date(1990, 1, 1) + datetime.timedelta(
                days=random.randint(0, 15000))
            jy, jm, jd = to_jalaali(d.year, d.month, d.day)
            out = subprocess.run(
                ["jdate", "-j", f"{d.year}/{d.month:02d}/{d.day:02d}",
                 "+%Y/%m/%d"],
                capture_output=True, text=True)
            self.assertIn(f"{jy}/{jm:02d}/{jd:02d}", out.stdout,
                          f"اختلاف با libjalali برای {d}")

    def test_fa_digits(self):
        self.assertEqual(fa_digits("1405/6/28"), "۱۴۰۵/۶/۲۸")
        self.assertEqual(fa_digits(1234567890), "۱۲۳۴۵۶۷۸۹۰")

    def test_names(self):
        self.assertEqual(jalaali_month_name(6), "شهریور")
        self.assertEqual(jalaali_month_name(12), "اسفند")
        self.assertEqual(jalaali_weekday_name(2026, 9, 19), "شنبه")

    def test_leap(self):
        self.assertTrue(is_jalaali_leap(1403))
        self.assertFalse(is_jalaali_leap(1404))


if __name__ == "__main__":
    unittest.main(verbosity=2)
