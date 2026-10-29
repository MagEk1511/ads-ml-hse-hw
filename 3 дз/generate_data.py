import numpy as np
import pandas as pd


COURSES = [
    ("PY101", "Python: основы", "Программирование", 24, 4900),
    ("DA201", "Анализ данных", "Data Science", 32, 7900),
    ("ML301", "Основы ML", "Data Science", 36, 9900),
    ("SQL201", "SQL и базы данных", "Базы данных", 28, 6900),
    ("WEB101", "Web-разработка", "Программирование", 30, 7500),
]

REGIONS = ["Москва", "Санкт-Петербург", "Поволжье", "Урал", "Сибирь"]
DEVICES = ["Desktop", "Mobile", "Tablet"]
SUBSCRIPTIONS = ["Разовая оплата", "Месячная", "Корпоративная"]
STATUSES = ["active", "completed", "dropped"]


def generate_learning_data(variant: int, rows: int = 240):
    rng = np.random.default_rng(20261015 + variant)

    course_catalog = pd.DataFrame(
        COURSES,
        columns=["course_id", "course_name", "course_category", "lessons_total", "base_price"]
    )

    student_ids = rng.integers(2000, 2120, size=rows)
    course_ids = rng.choice(course_catalog["course_id"], size=rows)
    course_map = course_catalog.set_index("course_id")

    start_base = np.datetime64("2026-02-01")
    start_dates = start_base + rng.integers(0, 180, size=rows).astype("timedelta64[D]")

    total_lessons = np.array([course_map.loc[c, "lessons_total"] for c in course_ids])
    progress = np.clip(rng.beta(2.2, 1.6, size=rows), 0, 1)
    completed_lessons = np.rint(total_lessons * progress).astype(float)

    study_hours = np.maximum(
        0,
        completed_lessons * rng.normal(0.9, 0.18, size=rows)
        + rng.normal(0, 2, size=rows)
    )

    score = np.clip(
        45 + progress * 50 + rng.normal(0, 9, size=rows),
        0, 100
    )

    last_activity = start_dates + np.rint(
        np.maximum(1, study_hours * 1.8 + rng.normal(5, 7, size=rows))
    ).astype("timedelta64[D]")

    status = np.where(
        progress >= 0.95,
        "completed",
        np.where(progress < 0.25, "dropped", "active")
    )

    df = pd.DataFrame({
        "student_id": student_ids,
        "course_id": course_ids,
        "start_date": start_dates.astype("datetime64[D]").astype(str),
        "last_activity": last_activity.astype("datetime64[D]").astype(str),
        "lessons_completed": completed_lessons,
        "study_hours": np.round(study_hours, 2),
        "score": np.round(score, 2),
        "subscription": rng.choice(SUBSCRIPTIONS, size=rows, p=[0.45, 0.38, 0.17]),
        "region": rng.choice(REGIONS, size=rows),
        "device": rng.choice(DEVICES, size=rows, p=[0.58, 0.35, 0.07]),
        "status": status,
    })

    # Пропуски
    for col, n in [("score", 7), ("study_hours", 5), ("region", 4), ("device", 3)]:
        idx = rng.choice(df.index, size=n, replace=False)
        df.loc[idx, col] = np.nan

    # Некорректные значения
    invalids = {
        "lessons_completed": [-3, 999],
        "study_hours": [-5],
        "score": [-10, 135],
    }
    for col, vals in invalids.items():
        idx = rng.choice(df.index, size=len(vals), replace=False)
        for i, val in zip(idx, vals):
            df.loc[i, col] = val

    # Некорректные даты
    for col in ["start_date", "last_activity"]:
        idx = rng.choice(df.index, size=2, replace=False)
        df.loc[idx[0], col] = "not_a_date"
        df.loc[idx[1], col] = "31.02.2026"

    # Грязные категории
    idx = rng.choice(df.index, size=5, replace=False)
    dirty_sub = [" месячная ", "РАЗОВАЯ ОПЛАТА", "корпоративная", "Месячная ", " разовая оплата"]
    for i, v in zip(idx, dirty_sub):
        df.loc[i, "subscription"] = v

    idx = rng.choice(df.index, size=4, replace=False)
    dirty_dev = ["desktop ", "MOBILE", " tablet", "Desktop "]
    for i, v in zip(idx, dirty_dev):
        df.loc[i, "device"] = v

    # Полные дубликаты
    dup = df.sample(5, random_state=variant)
    df = pd.concat([df, dup], ignore_index=True)
    df = df.sample(frac=1, random_state=variant).reset_index(drop=True)

    return df, course_catalog


def main():
    print("=" * 60)
    print("Генератор домашнего датасета: онлайн-обучение")
    print("=" * 60)
    variant = int(input("Введите номер варианта: "))

    activity, courses = generate_learning_data(variant)
    activity.to_csv("learning_activity.csv", index=False, encoding="utf-8-sig")
    courses.to_csv("courses.csv", index=False, encoding="utf-8-sig")

    print()
    print("Созданы:")
    print("learning_activity.csv")
    print("courses.csv")


if __name__ == "__main__":
    main()
