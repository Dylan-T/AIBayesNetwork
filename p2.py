import sys

# Take inputs
if len(sys.argv) == 2:
    train = sys.argv[0]
    test = sys.argv[1]
else:
    train = "ass3DataFiles/part1/spamLabelled.dat"
    test = "ass3DataFiles/part1/spamUnlabelled.dat"

# Load Data
trainData = open(train, "r").read().splitlines()
for i in range(0, len(trainData)):
    trainData[i] = trainData[i].split()
    for feature in range(len(trainData[i])):
        trainData[i][feature] = int(trainData[i][feature])


testData = open(test, "r").read().splitlines()
for i in range(0, len(testData)):
    testData[i] = testData[i].split()
    for feature in range(len(testData[i])):
        testData[i][feature] = int(testData[i][feature])

# Bayes rules:
# P(class| data) = P(data|class)*P(class) / P(data)
# denominator can be ignored?

# Build Table
# |Class|1|0|
# |-----|-|-|
# |Total|6|6|
# |f[0] F|3|2|
# |f[0] T|3|2|
# |f[1] F|3|2|
# |f[1] T|3|2|
# ...

# Create table for n features
table = [[1, 1] for n in range(len(trainData[0])*2 - 1)]

# Count occurrences
for sample in trainData:
    i = 0
    while i < len(table) - 1:
        i = i + sample[int(i/2)]
        table[i][sample[len(sample)-1]] = table[i][sample[len(sample)-1]] + 1
        i = i + 2 - (i % 2)  # iterate to next feature
    table[len(table)-1][sample[len(sample)-1]] = table[len(table)-1][sample[len(sample)-1]] + 1  # add to class count

# Classify:

for sample in testData:
    # calculate P(class1|data)  == P(data|class1)*P
    p1 = 1
    i = 0
    while i < len(table) - 1:
        i = i + sample[int(i / 2)]
        p1 = p1 * table[i][0] / table[len(table)-1][0]
        i = i + 2 - (i % 2)  # iterate to next feature
    p1 = p1*(table[len(table)-1][0]/(table[len(table)-1][0]+table[len(table)-1][1]))

    # calculate P(class1|data)  == P(data|class1)*P
    p2 = 1
    i = 0
    while i < len(table) - 1:
        i = i + sample[int(i / 2)]
        p2 = p2 * table[i][1] / table[len(table)-1][1]
        i = i + 2 - (i % 2)  # iterate to next feature
    p2 = p2*(table[len(table)-1][1]/(table[len(table)-1][0]+table[len(table)-1][1]))

    # return class with higher P
    print(p1)
    print(p2)
