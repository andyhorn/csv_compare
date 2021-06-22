import csv
import sys
import os
import getopt

PATH = ''
HEADERS = []
ROWS = []
DIFFERENCES = []
TARGETS = []

DIFFERENCES_HEADER = 'Differences'
SIMILARITIES_HEADER = 'Similarities'
ITEM_DELIMITER = ' '


def header(num):
    return HEADERS[TARGETS[num]]


def read_csv():
    global HEADERS
    global ROWS

    with open(PATH) as file:
        reader = csv.DictReader(file, delimiter=',')
        HEADERS = reader.fieldnames
        for row in reader:
            ROWS.append(row)


def prep_line(line):
    return line.lower().replace('_', ' ').split()


def find_difference(left, right):
    left = prep_line(left)
    right = prep_line(right)
    differences = []
    for word in left:
        if word not in right and word not in differences:
            differences.append(word)
    return differences


def find_similarities(left, right):
    left = prep_line(left)
    right = prep_line(right)
    similarities = []

    for word in left:
        if word in right and word not in similarities:
            similarities.append(word)
    return similarities


def write_results():
    global HEADERS
    global ROWS

    if DIFFERENCES_HEADER not in HEADERS:
        HEADERS.append(DIFFERENCES_HEADER)
    if SIMILARITIES_HEADER not in HEADERS:
        HEADERS.append(SIMILARITIES_HEADER)

    with open(PATH, 'w') as file:
        writer = csv.DictWriter(file, delimiter=',', fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(ROWS)


def find_all_differences():
    for row in ROWS:
        left = row[header(0)]
        right = row[header(1)]

        differences = find_difference(left, right)
        differences.extend([x for x in find_difference(right, left) if x not in differences])

        row[DIFFERENCES_HEADER] = ITEM_DELIMITER.join(differences)


def find_all_similarities():
    for row in ROWS:
        left = row[header(0)]
        right = row[header(1)]

        similarities = find_similarities(left, right)
        similarities.extend([x for x in find_similarities(right, left) if x not in similarities])

        row[SIMILARITIES_HEADER] = ITEM_DELIMITER.join(similarities)


def main():
    print('Reading file:', PATH)
    read_csv()

    print('Scanning for column differences...')
    find_all_differences()

    print('Scanning for column similarities...')
    find_all_similarities()

    print('Writing results...')
    write_results()

    print('Done!')


def print_usage():
    print('csv_compare.py <filename> -c <cols>')
    print('\tex: csv_compare.py /path/to/file.csv -c 4,5')


def parse_args(args):
    global TARGETS
    global PATH

    if not len(args) > 1:
        print('Not enough arguments!')
        print_usage()
        sys.exit(1)

    PATH = args[0]

    if not os.path.exists(PATH):
        print('Could not find file: ', PATH)
        sys.exit(1)

    print(args[1:])

    try:
        options, arguments = getopt.getopt(args[1:], "hc:", ["cols="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in options:
        print(opt)
        print(arg)
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-c', '--cols'):
            if ',' not in arg:
                print_usage()
                sys.exit(2)
            else:
                TARGETS = [int(x) for x in arg.split(',')]
        else:
            print('Invalid argument: ', opt)


if __name__ == '__main__':
    parse_args(sys.argv[1:])
    main()
