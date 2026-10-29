import numpy as np


def generate_dataset(variant: int, rows: int = 120) -> np.ndarray:
    rng = np.random.default_rng(20260927 + variant)

    distance = rng.uniform(0.8, 30, size=rows)
    delivery_type = rng.integers(0, 2, size=rows)

    wait_time = rng.normal(loc=8, scale=4, size=rows)
    wait_time = np.clip(wait_time, 0, 30)

    duration = (
        12
        + distance * 2.2
        + wait_time * 0.5
        - delivery_type * 5
        + rng.normal(0, 5, size=rows)
    )
    duration = np.clip(duration, 8, 120)

    order_amount = rng.lognormal(mean=8.0, sigma=0.55, size=rows)
    order_amount = np.clip(order_amount, 500, 20000)

    expected_time = 15 + distance * 2
    delay = np.maximum(duration - expected_time, 0)

    rating = (
        4.8
        - delay * 0.025
        - wait_time * 0.025
        + rng.normal(0, 0.25, size=rows)
    )
    rating = np.clip(rating, 1, 5)

    data = np.column_stack(
        (distance, duration, order_amount, wait_time, rating, delivery_type)
    )
    data = np.round(data, 2)

    used_rows = set()

    def unique_row():
        while True:
            row = int(rng.integers(0, rows))
            if row not in used_rows:
                used_rows.add(row)
                return row

    for _ in range(4):
        row = unique_row()
        col = int(rng.integers(0, 5))
        data[row, col] = np.nan

    row = unique_row()
    data[row, 2] = np.inf

    row = unique_row()
    data[row, 0] = -12

    row = unique_row()
    data[row, 1] = -25

    row = unique_row()
    data[row, 2] = -3500

    row = unique_row()
    data[row, 3] = -15

    row = unique_row()
    data[row, 4] = 8

    row = unique_row()
    data[row, 1] = 180

    row = unique_row()
    data[row, 2] = 35000

    return data


def save_dataset(data: np.ndarray) -> None:
    np.save("delivery_data.npy", data)
    np.savetxt(
        "delivery_data.csv",
        data,
        delimiter=";",
        fmt="%.2f",
        header="distance_km;duration_min;order_amount;wait_min;rating;delivery_type",
        comments="",
    )


def main():
    print("=" * 55)
    print("Генератор данных службы доставки")
    print("=" * 55)

    variant = int(input("Введите номер варианта: "))
    data = generate_dataset(variant)
    save_dataset(data)

    print()
    print("Набор данных успешно создан.")
    print("Количество доставок:", data.shape[0])
    print("Количество признаков:", data.shape[1])
    print()
    print("Созданы файлы:")
    print("delivery_data.npy")
    print("delivery_data.csv")


if __name__ == "__main__":
    main()
