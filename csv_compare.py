import csv
import sys

HEADERS = []
ROWS = []
DIFFERENCES = []
TARGETS = ['five', 'six']

DIFFERENCES_HEADER = 'Differences'
SIMILARITIES_HEADER = 'Similarities'
ITEM_DELIMITER = ' '


def read_csv(path):
    global HEADERS
    global ROWS

    with open(path) as file:
        reader = csv.DictReader(file, delimiter=',')
        HEADERS = reader.fieldnames
        for row in reader:
            ROWS.append(row)

    print(HEADERS)
    print(ROWS)


def prep_line(line):
    return line.lower().replace('_', ' ').split()


def find_difference(left, right):
    print('finding difference between:')
    print(left)
    print(right)
    left = prep_line(left)
    right = prep_line(right)
    differences = []
    for word in left:
        if word not in right and word not in differences:
            differences.append(word)
    print(differences)
    return differences


def find_similarities(left, right):
    print('finding similarities between:')
    print(left)
    print(right)
    left = prep_line(left)
    right = prep_line(right)
    similarities = []

    for word in left:
        if word in right and word not in similarities:
            similarities.append(word)
    print(similarities)
    return similarities


def write_results(path):
    global HEADERS
    global ROWS

    if DIFFERENCES_HEADER not in HEADERS:
        HEADERS.append(DIFFERENCES_HEADER)
    if SIMILARITIES_HEADER not in HEADERS:
        HEADERS.append(SIMILARITIES_HEADER)

    with open(path, 'w') as file:
        writer = csv.DictWriter(file, delimiter=',', fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(ROWS)


def find_all_differences():
    for row in ROWS:
        left = row[TARGETS[0]]
        right = row[TARGETS[1]]

        differences = find_difference(left, right)
        differences.extend([x for x in find_difference(right, left) if x not in differences])

        row[DIFFERENCES_HEADER] = ITEM_DELIMITER.join(differences)


def find_all_similarities():
    for row in ROWS:
        left = row[TARGETS[0]]
        right = row[TARGETS[1]]

        similarities = find_similarities(left, right)
        similarities.extend([x for x in find_similarities(right, left) if x not in similarities])

        row[SIMILARITIES_HEADER] = ITEM_DELIMITER.join(similarities)


def main():
    path = sys.argv[1]
    print('finding differences in file:', path)
    read_csv(path)
    find_all_differences()
    find_all_similarities()
    write_results(path)


main()
