
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]

yearList = list()
dayList = list()
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    count = 0
    for row in csv_reader:
        count += 1
        if count == 1:
            continue
        yearList.append(int(row[0]))
        dayList.append(int(row[1]))

plt.xlabel('Year')
plt.ylabel('Number of frozen days')

plt.plot(yearList, dayList)
plt.savefig("plot1.jpg")
#print(yearList)
#print(dayList)
def q3a():
    xList =list()
    for year in yearList:
        newList = np.array([1, year])
        #print(newList)
        xList.append(newList)

    xList = np.array(xList)
    return (xList)

print("Q3a:")
xList = q3a()
print(xList)

def q3b():
    yList = list()
    for day in dayList:
        yList.append(day)

    yList = np.array(yList)
    return yList

print("Q3b:")
yList = q3b()
print(yList)


def q3c(X):
    return np.dot(np.transpose(X), X)

print("Q3c:")
xTranspose  = q3c(xList)
print(xTranspose)

def q3d(xTrans):
    return np.linalg.inv(xTrans)

print("Q3d:")
xInv = q3d(xTranspose)
print(xInv)

def q3e(X, xInv):
    return np.dot(xInv, np.transpose(X))

print("Q3e:")
piX = q3e(xList, xInv)
print(piX)

def q3f(piX, yList):
    return np.dot(piX, yList)

print("Q3f:")
beta = q3f(piX, yList)
print(beta)

def q4(beta):
    return beta[0] + beta[1] * 2021

print("Q4: " + str((q4(beta))))

def q5(beta):
    if beta[1] > 0:
        return '>'
    elif beta[1] < 0:
        return '<'
    else:
        return '='

print("Q5a: " + q5(beta))
print("Q5b: This sign indicates the whether the time period for the amount of days Lake Mendota"
      "stays frozen increases, decrease, or stays the same. When the sign if >, this means that "
      "the amount of time Lake Mendota is frozen increases. When the sign is <, this means that "
      "the amount of time Lake Mendota is frozen decreases. When the sign is =, this means that "
      "the amount of time Lake Mendota is frozen stays the same. ")

def q6(beta):
    return ((beta[0] * -1) / beta[1])

print("Q6a: " + str(q6(beta)))
print("Q6b: x* is a compelling prediction as based of the data, the data shows that the number of days that Lake Mendota"
      " stays frozen is decreasing as time goes on "
      "On top of that, the MLE function we used has a negative sloop, which means that number of days that Lake Mendota "
      "stays frozen will decrease, and eventually not freeze.")