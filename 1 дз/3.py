from functools import lru_cache


def calculate_balances(names: list[str], expenses: dict) -> list[int]:
    total = sum(expenses.values()) * 100
    average, remainder = divmod(total, len(names))

    balances = []

    for i, name in enumerate(names):
        share = average + (1 if i < remainder else 0)
        balances.append(expenses[name] * 100 - share)

    return balances


def settle_debts(names: list[str], balances: list[int]) -> list:
    participants = []

    for i in range(len(names)):
        if balances[i] != 0:
            participants.append((names[i], balances[i]))

    names = [name for name, balance in participants]
    initial_balances = tuple(balance for name, balance in participants)

    @lru_cache(maxsize=None)
    def backtracking(state: tuple) -> tuple:
        i = 0

        while i < len(state) and state[i] == 0:
            i += 1

        if i == len(state):
            return ()

        best = None
        checked = set()

        for j in range(i + 1, len(state)):
            if state[i] * state[j] >= 0:
                continue

            if state[j] in checked:
                continue

            checked.add(state[j])

            new_state = list(state)
            new_state[j] += new_state[i]
            new_state[i] = 0

            if state[i] < 0:
                transfer = (names[i], names[j], -state[i])
            else:
                transfer = (names[j], names[i], state[i])

            result = backtracking(tuple(new_state))
            transfers = (transfer,) + result

            if best is None or len(transfers) < len(best):
                best = transfers

            if state[i] + state[j] == 0:
                break

        return best

    return list(backtracking(initial_balances))


if __name__ == '__main__':
    names = input().split()
    n = int(input())

    expenses = {name: 0 for name in names}

    for _ in range(n):
        name, amount = input().split()
        expenses[name] += int(amount)

    balances = calculate_balances(names, expenses)
    transfers = settle_debts(names, balances)

    print(len(transfers))

    for sender, receiver, amount in transfers:
        print(sender, receiver, f'{amount / 100:.2f}')
