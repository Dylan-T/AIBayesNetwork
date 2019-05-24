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
    # Create table for n features
    table = [[1, 1, 2] for n in range(len(data[0])*2 - 1)]
    # Count occurrences
    for sample in data:
        i = 0
        while i < len(table) - 1:
            i = i + sample[int(i/2)]
            table[i][sample[len(sample)-1]] = table[i][sample[len(sample)-1]] + 1
            table[i][2] = table[i][2] + 1
            i = i + 2 - (i % 2)  # iterate to next feature
        table[len(table)-1][sample[len(sample)-1]] = table[len(table)-1][sample[len(sample)-1]] + 1 # add to class count
        table[len(table) - 1][2] = table[len(table) - 1][2] + 1
    return table


def create_prob_table(table):
    # Create probability table
    pTable = [[1, 1, 1] for n in range(len(table))]
    for i in range(0, len(pTable)-1):
        for clazz in range(3):
            pTable[i][clazz] = table[i][clazz] / table[len(table)-1][clazz]
    pTable[len(pTable)-1][0] = table[len(table)-1][0] / table[len(table)-1][2]
    pTable[len(pTable)-1][1] = table[len(table)-1][1] / table[len(table)-1][2]
    return pTable


def classify(sample, pTable):
    # calculate P(class|data)  == (P(data|class)*P(class)) / p(data)
    p1 = 1  # P(data|class1)
    p2 = 1  # P(data|class2)
    i = 0
    while i < len(pTable) - 1:
        i = i + sample[int(i / 2)]
        p1 = p1 * pTable[i][0]
        p2 = p2 * pTable[i][1]
        i = i + 2 - (i % 2)  # iterate to next feature
    p1 = (p1*pTable[len(pTable)-1][0])
    p2 = (p2*pTable[len(pTable)-1][1])

    # return class with higher P
    if p1 > p2:
        return 0
    else:
        return 1


# Take inputs
if len(sys.argv) == 2:
    train = load_data(sys.argv[0])
    test = load_data(sys.argv[1])
else:
    train = load_data("ass3DataFiles/part1/spamLabelled.dat")
    test = load_data("ass3DataFiles/part1/spamUnlabelled.dat")

table = create_table(train)
pTable = create_prob_table(table)

results = []
for sample in test:
    results.append(classify(sample, pTable))

print(results)
