"""Sandwalker pocket data"""

import collections
import time


def make_entries_by_month(entries):
    """Sort entries by month.

    This is a bit convoluted (could use explicit objects) but we want
    to support at some point a JSON API easily, where having a raw
    dict will be easier.
    """
    r = dict()

    current_date = None
    total = 0
    count = 0

    for entry in entries:
        current_date = entry.time.strftime("%Y-%m-01")

        if not current_date in r:
            r[current_date] = {
                'month_total': 0,
                'entries': []
            }

        count += 1
        total += entry.amount

        r[current_date]['month_total'] += entry.amount
        r[current_date]['entries'].append({
            'current_total': total,
            'current_count': count,
            'current_month_total': r[current_date]['month_total'],
            'block': entry.block,
            'amount': entry.amount
        })

    return count, total, r
