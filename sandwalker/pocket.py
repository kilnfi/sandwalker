"""Sandwalker pocket data"""

import collections

# This is temporary for now, and to be moved to the database at some
# point. Alternatively, we could also store the timestamp of the block
# in the database.
#
# This was computed using https://github.com/aimxhaisse/pocket_counter_experiments
BLOCK_DATES = {
    '2020-07-01': [1, 324],
    '2020-08-01': [325, 3294],
    '2020-09-01': [3295, 6121],
    '2020-10-01': [6122, 9009],
    '2020-11-01': [9010, 11795],
    '2020-12-01': [11796, 14690],
    '2021-01-01': [14691, 17379],
    '2021-02-01': [17380, 19704],
    '2021-03-01': [19705, 22182],
    '2021-04-01': [22183, 24740],
    '2021-05-01': [24741, 100000],
}

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

        if not current_date or entry.block > BLOCK_DATES[current_date][1]:
            for key, values in BLOCK_DATES.items():
                if entry.block >= values[0] and entry.block <= values[1]:
                    current_date = key
                    r[current_date] = {
                        'month_total': 0,
                        'entries': []
                    }
                    break

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
