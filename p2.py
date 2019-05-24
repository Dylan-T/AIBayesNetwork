import sys


def load_data(filename):
    # Load Data
    data = open(filename, "r").read().splitlines()
    for i in range(0, len(data)):
        data[i] = data[i].split()
        for feature in range(len(data[i])):
            data[i][feature] = int(data[i][feature])
    return data


def create_table(data):
    n_rows = len(data[0])*2 - 1

    # Create table for n features
    table = [[1, 1] for n in range(n_rows-1)]
    table.append([2, 2])
    # Count occurrences
    for sample in data:
        s_class = sample[len(sample)-1]
        i = 0
        while i < n_rows - 1:
            i = i + sample[int(i/2)]
            table[i][s_class] = table[i][s_class] + 1
            i = i + 2 - (i % 2)  # iterate to next feature
        table[n_rows-1][s_class] = table[n_rows-1][s_class] + 1  # add to class count
    return table


def create_prob_table(table):
    # Create probability table
    n_rows = len(table)
    pTable = [[1, 1] for n in range(n_rows)]
    for i in range(0, n_rows-1):
        for clazz in range(2):
            pTable[i][clazz] = table[i][clazz] / table[n_rows-1][clazz]
    pTable[n_rows-1][0] = table[n_rows-1][0] / (table[n_rows-1][0] + table[n_rows-1][1])
    pTable[n_rows-1][1] = table[n_rows-1][1] / (table[n_rows-1][0] + table[n_rows-1][1])
    return pTable


def classify(sample, pTable):
    # calculate P(class|data)  == (P(data|class)*P(class))
    n_rows = len(pTable)
    p0 = pTable[n_rows-1][0]
    p1 = 1 - p0
    i = 0
    while i < n_rows - 1:
        i = i + sample[int(i / 2)]
        p0 = p0 * pTable[i][0]
        p1 = p1 * pTable[i][1]
        i = i + 2 - (i % 2)  # iterate to next feature
    # return class with higher P
    print("Instance " + str(c) + ":")
    print("Input: " + str(sample))
    print("P(S|D): " + str(p1))
    print("P(!S|D): " + str(p0))
    if p0 > p1:
        print("Class: Not Spam")
    else:
        print("Class: Spam")
    print()
    if p0 > p1:
        return 0
    else:
        return 1


def log_tables(table, pTable):
    file = open("log.txt", "w")
    file.write("Occurrence table: \n")
    for i in range(len(table)):
        file.write(str(table[i]))
        file.write("\n")

    file.write("Probability table:\n")
    for i in range(len(pTable)):
        file.write(str(pTable[i]))
        file.write("\n")


# Take inputs
if len(sys.argv) == 2:
    train = load_data(sys.argv[0])
    test = load_data(sys.argv[1])
else:
    train = load_data("ass3DataFiles/part1/spamLabelled.dat")
    test = load_data("ass3DataFiles/part1/spamUnlabelled.dat")

table = create_table(train)
pTable = create_prob_table(table)

log_tables(table, pTable)
global c
c = 1
results = []
for sample in test:
    results.append(classify(sample, pTable))
    c += 1

print(results)
file = open("sampleoutput.txt", "w")
file.write(str(results))
