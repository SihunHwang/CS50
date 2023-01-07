import sys
import csv


def main():
    # check for valid command line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data sequence")
        sys.exit()

    # open database
    with open(sys.argv[1], 'r') as database:
        data = list(csv.DictReader(database))

        STRs = list(data[0].keys())
        STRs.remove('name')

    with open(sys.argv[2], 'r') as file:
        dna = file.read()

    # find match
    counts = {}
    for STR in STRs:

        count = 0
        for i in range(len(dna)):

            cursor = 0
            while i + cursor < len(dna):

                if dna[i + cursor] != STR[cursor % len(STR)]:
                    break

                cursor += 1

            count = max((cursor // len(STR)), count)

        counts[STR] = count

    for person in data:

        match = True
        for STR in counts:

            if counts[STR] != int(person[STR]):
                match = False
                break

        if match:
            print(person['name'])
            return person['name']

    print('No match')
    return 'No match'


if __name__ == '__main__':
    main()