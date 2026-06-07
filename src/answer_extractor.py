#!/usr/bin/env python3
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Optional

_NUMBER_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
_BOXED_RE = re.compile(r"\\boxed\{([^{}]+)\}")
_HASH_RE = re.compile(r"####\s*([-+]?\d[\d,]*(?:\.\d+)?)")


def normalize_number(text) -> Optional[str]:
    if text is None:
        return None
    raw = str(text).replace(",", "").replace("$", "").replace("%", "").strip()
    m = _NUMBER_RE.search(raw)
    if not m:
        return None
    raw = m.group(0)
    try:
        d = Decimal(raw)
    except InvalidOperation:
        return raw
    if d == d.to_integral_value():
        return str(int(d))
    return format(d.normalize(), "f").rstrip("0").rstrip(".")


def extract_answer(text: str) -> Optional[str]:
    if not text:
        return None
    m = list(_HASH_RE.finditer(text))
    if m:
        return normalize_number(m[-1].group(1))
    m = list(_BOXED_RE.finditer(text))
    if m:
        return normalize_number(m[-1].group(1))
    marker = list(re.finditer(r"(?:final answer|answer)\s*(?:is|=|:)\s*([-+]?\d[\d,]*(?:\.\d+)?)", text, re.I))
    if marker:
        return normalize_number(marker[-1].group(1))
    nums = _NUMBER_RE.findall(text)
    return normalize_number(nums[-1]) if nums else None
