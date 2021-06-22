import csv
import sys
import os
import getopt

PATH = ''
HEADERS = []
ROWS = []
DIFFERENCES = []
TARGETS = []
TARGET_IS_STRING = False

DIFFERENCES_HEADER = 'x_Differences'
SIMILARITIES_HEADER = 'x_Similarities'
ITEM_DELIMITER = ';'


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


def get_headers():
    return [get_header(TARGETS[0]), get_header(TARGETS[1])]


def get_header(val):
    if can_parse_int(val):
        col = HEADERS[int(val)]
        return col

    return val


def find_all_differences():
    headers = get_headers()

    for row in ROWS:
        left = row[headers[0]]
        right = row[headers[1]]

        differences = find_difference(left, right)
        differences.extend([x for x in find_difference(right, left) if x not in differences])

        row[DIFFERENCES_HEADER] = ITEM_DELIMITER.join(differences)


def find_all_similarities():
    headers = get_headers()

    for row in ROWS:
        left = row[headers[0]]
        right = row[headers[1]]

        similarities = find_similarities(left, right)
        similarities.extend([x for x in find_similarities(right, left) if x not in similarities])

        row[SIMILARITIES_HEADER] = ITEM_DELIMITER.join(similarities)


def main():
    print('File:', PATH)
    read_csv()

    print('Detecting differences...')
    find_all_differences()

    print('Detecting similarities...')
    find_all_similarities()

    print('Writing results...')
    write_results()

    print('Done!')


def print_usage():
    print('csv_compare.py <filename> -c <cols>')
    print('\tex: csv_compare.py /path/to/file.csv -c 4,5')


def can_parse_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def parse_args(args):
    global TARGETS
    global TARGET_IS_STRING
    global PATH

    if not len(args) > 1:
        print('Not enough arguments!')
        print_usage()
        sys.exit(1)

    PATH = args[0]

    if not os.path.exists(PATH):
        print('Could not find file: ', PATH)
        sys.exit(1)

    try:
        options, arguments = getopt.getopt(args[1:], "hc:", ["cols="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in options:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-c', '--cols'):
            if ',' not in arg:
                print_usage()
                sys.exit(2)
            else:
                TARGETS = arg.split(',')
                print(f'Comparing column \'{TARGETS[0]}\' to column \'{TARGETS[1]}\'')
        else:
            print('Invalid option: ', opt)
            print_usage()
            sys.exit(2)


if __name__ == '__main__':
    parse_args(sys.argv[1:])
    main()
