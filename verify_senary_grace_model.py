from datetime import date, timedelta

for year in (1810, 1812):
    starts = [
        ('S1', date(year, 1, 1)),
        ('S2', date(year, 3, 3)),
        ('S3', date(year, 5, 3)),
        ('S4', date(year, 7, 3)),
        ('S5', date(year, 9, 2)),
        ('S6', date(year, 11, 2)),
    ]
    print(f'{year} ({"leap" if year % 4 == 0 else "common"})')
    for index, (label, start) in enumerate(starts):
        end_exclusive = start + timedelta(days=60)
        next_start = starts[index + 1][1] if index + 1 < len(starts) else date(year + 1, 1, 1)
        gap_days = (next_start - end_exclusive).days
        print(f'{label}: {start.isoformat()} through {(end_exclusive - timedelta(days=1)).isoformat()}; gap before next = {gap_days} day(s)')
    print()
