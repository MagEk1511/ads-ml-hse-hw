"""Генератор учебного датасета по заказам интернет-магазина.

Установка: pip install numpy pandas
Запуск: python generate_data.py
Иные параметры: python generate_data.py --rows 12000 --seed 17 --output my_orders.csv

Каждая строка — один заказ; revenue — сумма заказа после скидки,
но ДО обработки возвратов. Пропуски rating/delivery_days созданы намеренно.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def generate_orders(rows: int = 8500, seed: int = 2026) -> pd.DataFrame:
    if rows < 100:
        raise ValueError('Количество заказов должно быть не меньше 100')
    rng = np.random.default_rng(seed)
    dates = pd.date_range('2025-01-01', '2025-12-31', freq='D')
    season = {1: .83, 2: .85, 3: .94, 4: .96, 5: 1.01, 6: 1.05,
              7: 1.15, 8: 1.07, 9: 1.10, 10: 1.18, 11: 1.72, 12: 1.43}
    weights = np.array([season[t.month] * (.84 if t.dayofweek >= 5 else 1.06)
                        for t in dates], dtype=float)
    weights /= weights.sum()
    selected_dates = rng.choice(dates, size=rows, p=weights)

    categories = ['Электроника', 'Одежда', 'Дом', 'Книги', 'Спорт', 'Красота']
    cat = rng.choice(categories, rows, p=[.18, .22, .20, .12, .14, .14])
    regions = rng.choice(['Центр', 'Северо-Запад', 'Юг', 'Урал', 'Сибирь'],
                         rows, p=[.36, .18, .19, .13, .14])
    channels = rng.choice(['Сайт', 'Приложение', 'Маркетплейс'],
                          rows, p=[.38, .36, .26])
    segments = rng.choice(['Новый', 'Постоянный', 'VIP'],
                          rows, p=[.48, .42, .10])
    units = np.clip(rng.poisson(1.15, rows) + 1, 1, 8)
    base_price = {'Электроника': 12400, 'Одежда': 3200, 'Дом': 4300,
                  'Книги': 850, 'Спорт': 5700, 'Красота': 1700}
    unit_price = np.array([base_price[c] for c in cat]) * rng.lognormal(0, .32, rows)
    premium = rng.random(rows) < .007
    unit_price[premium] *= rng.uniform(2.5, 4.3, premium.sum())
    unit_price = np.round(unit_price, -1)

    discount = np.round(np.clip(rng.beta(1.45, 7.2, rows) * .49
                        + np.where(pd.DatetimeIndex(selected_dates).month.isin([11, 12]), .045, 0),
                        0, .50), 2)
    discount = np.where(segments == 'VIP', np.minimum(.5, discount + .035), discount)
    revenue = np.round(units * unit_price * (1 - discount), 2)

    base_delivery = {'Центр': 2.5, 'Северо-Запад': 3.5, 'Юг': 4.0,
                     'Урал': 5.0, 'Сибирь': 6.0}
    delivery = np.clip(np.round(np.array([base_delivery[r] for r in regions])
                                + rng.normal(0, 1.6, rows)
                                + .5 * (channels == 'Маркетплейс')).astype(float), 1, 15)
    very_late = rng.random(rows) < .018
    delivery[very_late] = rng.integers(15, 26, very_late.sum())
    ratings = np.clip(np.round(5.0 - .17 * np.maximum(0, delivery - 3)
                               + rng.normal(0, .63, rows)), 1, 5).astype(float)
    return_probability = np.clip(.032 + .011 * np.maximum(0, delivery - 5)
                                 + .025 * (cat == 'Одежда')
                                 + .018 * (discount > .25), 0, .38)
    returned = (rng.random(rows) < return_probability).astype(int)
    ratings = np.clip(ratings - returned * rng.integers(0, 2, rows), 1, 5).astype(float)

    # Учебные особенности: реальные пропуски, задержки и редкие дорогие заказы.
    ratings[rng.random(rows) < .11] = np.nan
    delivery[rng.random(rows) < .033] = np.nan
    df = pd.DataFrame({
        'order_date': selected_dates, 'region': regions, 'category': cat,
        'channel': channels, 'customer_segment': segments, 'units': units,
        'unit_price': unit_price, 'discount_pct': discount, 'revenue': revenue,
        'delivery_days': delivery, 'rating': ratings, 'returned': returned,
    }).sort_values('order_date', kind='stable').reset_index(drop=True)
    df.insert(0, 'order_id', [f'ORD-2025-{i:05d}' for i in range(1, rows + 1)])
    df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%d')
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rows', type=int, default=8500)
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('orders_2025.csv'))
    args = parser.parse_args()
    data = generate_orders(rows=args.rows, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.output, index=False, encoding='utf-8-sig')
    print(f'Создано {len(data)} заказов: {args.output.resolve()}')
    print('Пропуски:\n', data[['rating', 'delivery_days']].isna().sum().to_string())


if __name__ == '__main__':
    main()
