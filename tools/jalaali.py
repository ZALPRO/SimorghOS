#!/usr/bin/env python3
"""شیم توسعه: نسخهٔ رسمی موتور جلالی در درخت chroot زندگی می‌کند."""
import importlib.util
import os
import sys

_CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "config", "includes.chroot",
                      "usr", "share", "simorgh", "jalaali.py")
_spec = importlib.util.spec_from_file_location("simorgh_jalaali", _CANON)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["simorgh_jalaali"] = _mod
_spec.loader.exec_module(_mod)
globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("_")})
