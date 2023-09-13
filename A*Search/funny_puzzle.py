import heapq
from operator import ge
import copy
import numpy as np





def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    goalArr = np.zeros(shape=(3,3))

    for i in range(3):
        goalArr[0][i] = to_state[i]
    for i in range(3,6):
        goalArr[1][i-3] = to_state[i]
    for i in range(6,9):
        goalArr[2][i-6] = to_state[i]
    #print(goalArr)

    currArr = np.zeros(shape=(3,3))

    for i in range(3):
        currArr[0][i] = from_state[i]
    for i in range(3,6):
        currArr[1][i-3] = from_state[i]
    for i in range(6,9):
        currArr[2][i-6] = from_state[i]
    #print(currArr)

    distance = 0
    for i in range(3):
        for j in range(3):
            val = currArr[i][j]
            if val == 0:
                continue
            goalRow, goalCol = np.argwhere(goalArr == val)[0]
            #print(val, "current index ", i, j, "goal index", goalRow, goalCol, "distance is " , abs(i - goalRow) + abs(j - goalCol))
            distance += abs(i - goalRow) + abs(j - goalCol)
    
    return distance

testArr = [2,5,1,4,3,6,7,0,0]
test = get_manhattan_distance(testArr)
#print(test)


def get_succ_helper(state, row, col):
    possibleSucc = []
    
    if row != 0:
        tempArr = copy.deepcopy(state)
        tempArr[row][col] = tempArr[row-1][col]
        tempArr[row-1][col] = 0
        l = []
        for i in range(3):
            for j in range(3):
                l.append(int(tempArr[i][j]))
        if l not in possibleSucc:
            possibleSucc.append(l)
    if col != 2:
        tempArr = copy.deepcopy(state)
        tempArr[row][col] = tempArr[row][col+1]
        tempArr[row][col+1] = 0
        l = []
        for i in range(3):
            for j in range(3):
                l.append(int(tempArr[i][j]))
        if l not in possibleSucc:
            possibleSucc.append(l)
    if row != 2:
        tempArr = copy.deepcopy(state)
        tempArr[row][col] = tempArr[row+1][col]
        tempArr[row+1][col] = 0
        l = []
        for i in range(3):
            for j in range(3):
                l.append(int(tempArr[i][j]))
        if l not in possibleSucc:
            possibleSucc.append(l)
    if col != 0:
        tempArr = copy.deepcopy(state)
        tempArr[row][col] = tempArr[row][col-1]
        tempArr[row][col-1] = 0
        l = []
        for i in range(3):
            for j in range(3):
                l.append(int(tempArr[i][j]))
        if l not in possibleSucc:
            possibleSucc.append(l)
    return possibleSucc
def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    currArr = np.zeros(shape=(3,3))
    for i in range(3):
        currArr[0][i] = state[i]
    for i in range(3,6):
        currArr[1][i-3] = state[i]
    for i in range(6,9):
        currArr[2][i-6] = state[i]

    rowFirst, colFirst = np.argwhere(currArr == 0)[0]
    rowSecond, colSecond = np.argwhere(currArr == 0)[1]
    #print(rowFirst, colFirst)
    #print(rowSecond, colSecond)
    succ_statesFirst = get_succ_helper(currArr, rowFirst, colFirst)
    succ_statesSecond = get_succ_helper(currArr, rowSecond, colSecond)

    #print(succ_statesFirst)
    #print(succ_statesSecond)
    succ_states = []

    for x in succ_statesFirst:
        if x not in succ_states and x != state:
            succ_states.append(x)
    for x in succ_statesSecond:
        if x not in succ_states and x != state:
            succ_states.append(x)
    
    return sorted(succ_states)

l = [2,5,1,4,0,6,7,0,3]
#t = get_succ(l)
#print(t)

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)
    for succ_state in succ_states:
        #print(succ_state)
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))

#(print_succ(l))

def printParentHelper(closed, parent):
    currArr = copy.deepcopy(parent)
    moves = 0
    if currArr[2][2] != -1:
        for i in range(len(closed)):
            if closed[i][2][2] + 1 == currArr[2][2]:
                break
        moves = printParentHelper(closed[i], closed)
    
    print(currArr[1], 'h=%d' %get_manhattan_distance(currArr[1]), 'moves:', moves)
    return moves +1

def search_parent(par_num, CLOSED):
    for i in range (0, len(CLOSED)):
        if CLOSED[i][2][2]+1 == par_num:
            break
    return CLOSED[i]
    
## This function prints the solution of the puzzle
def print_sol(item, CLOSED):
    moves = 0
    cur = copy.deepcopy(item)
    if cur[2][2] != -1:
        #print(search_parent(cur[2][2],CLOSED))
        moves = print_sol(search_parent(cur[2][2],CLOSED),CLOSED)
    print(cur[1], 'h=%d' %get_manhattan_distance(cur[1]), 'moves:', moves)
    return moves + 1      

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    open, closed = [], []
    h, g = get_manhattan_distance(state), 0
    goalG, goalH, goalF = 0, 0, 0
    heapq.heappush(open, (g+h, state, (g, h, -1)))

    while open: 
        
        item = heapq.heappop(open)
        closed.append(item)

        hVal = item[2][1]
        if hVal == 0: #goal
            print_sol(item,closed)
            return 
        
        goalG = item[2][0] + 1
        currArr = get_succ(item[1])

        for i in range(len(currArr)):
            found, update = False, False

            goalH = get_manhattan_distance(currArr[i])

            for j in range(len(open)):
                if open[j][1] == currArr[i]:
                    currG = open[j][2][0]
                    if goalG < currG:
                        open.pop(j)
                        update= True
                    found = True
                    break

            for j in range(len(closed)):
                if closed[j][1] == currArr[i]:
                    currG = closed[j][2][0]
                    if goalG < currG:
                        update = True
                    found = True
                    break
            
            if not found or update:
                goalF = goalG + goalH
                heapq.heappush(open,(goalF,currArr[i],(goalG,goalH,item[2][2]+1)))
    return          




if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([2,5,1,4,0,6,7,0,3])
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()
