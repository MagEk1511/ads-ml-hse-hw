import re
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


DATE_PATTERN = (
    r'(?P<day>\d{1,2})(?P<date_sep>[./])'
    r'(?P<month>\d{1,2})(?P=date_sep)(?P<year>\d{4})'
)

PATTERNS = [
    re.compile(
        rf'^\s*{DATE_PATTERN}[\s,;]+'
        rf'(?P<name>.+)[\s,;]+'
        rf'(?P<price>\d+[.,]\d{{1,2}})\s*$'
    ),
    re.compile(
        rf'^\s*{DATE_PATTERN}[\s,;]+'
        rf'(?P<name>.+)[\s,;]+'
        rf'(?P<price>\d+)\s*$'
    )
]


def parse_order(line: str):
    for pattern in PATTERNS:
        match = pattern.fullmatch(line)

        if not match:
            continue

        name = match.group('name').strip()

        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        elif '"' in name:
            continue

        if not name:
            continue

        try:
            date = datetime(
                int(match.group('year')),
                int(match.group('month')),
                int(match.group('day'))
            ).date()
        except ValueError:
            continue

        price = Decimal(match.group('price').replace(',', '.'))

        return date, name, price

    return None


def analyze_orders(filename: str):
    pizza_counts = Counter()
    daily_totals = defaultdict(lambda: Decimal('0'))

    total = Decimal('0')
    count = 0
    most_expensive = None

    with open(filename, encoding='utf-8') as file:
        for line in file:
            order = parse_order(line)

            if order is None:
                continue

            date, name, price = order

            pizza_counts[name] += 1
            daily_totals[date] += price

            total += price
            count += 1

            if most_expensive is None or price > most_expensive[2]:
                most_expensive = order

    print('а)')
    for name, amount in pizza_counts.most_common():
        print(f'{name} - {amount}')

    print('\nб)')
    for date in sorted(daily_totals):
        print(date.strftime('%d.%m.%Y'), f'{daily_totals[date]:.2f}')

    print('\nв)')
    if most_expensive:
        date, name, price = most_expensive
        print(date.strftime('%d.%m.%Y'), name, f'{price:.2f}')

    print('\nг)')
    if count:
        average = (total / count).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )
        print(f'{average:.2f}')
    else:
        print('Нет корректных заказов')


if __name__ == '__main__':
    analyze_orders('orders.txt')
