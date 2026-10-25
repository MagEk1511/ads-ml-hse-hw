import requests

mbox = requests.get('https://www.py4e.com/code3/mbox.txt').text
all_lines = mbox.split('\n')


def get_authors(lines: list[str]) -> dict:
    authors = {}

    for line in lines:
        if line.startswith('From '):
            email = line.split()[1]

            if email not in authors:
                authors[email] = 0

            authors[email] += 1

    return authors


if __name__ == '__main__':
    authors = get_authors(all_lines)

    for email, count in authors.items():
        print(email, count)

    most_active = max(authors, key=authors.get)

    print('\nСамый активный автор:')
    print(most_active, authors[most_active])
