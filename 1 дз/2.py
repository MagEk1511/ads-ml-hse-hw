def get_median(numbers: list[int]) -> float:
    n = len(numbers)

    if n % 2 == 0:
        return (numbers[n // 2 - 1] + numbers[n // 2]) / 2

    return numbers[n // 2]


def get_invalid_ratio(numbers: list[int]) -> float:
    numbers.sort()
    n = len(numbers)

    middle = n // 2

    q1 = get_median(numbers[:middle])
    q3 = get_median(numbers[(n + 1) // 2:])

    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    invalid_count = 0

    for number in numbers:
        if number < lower_bound or number > upper_bound:
            invalid_count += 1

    return invalid_count


if __name__ == '__main__':
    n = int(input())
    numbers = []

    for _ in range(n):
        numbers.append(int(input()))

    print(get_invalid_ratio(numbers))
