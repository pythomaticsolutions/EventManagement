'''
                            -- breadth --
                   20         30         50        150
    ||     30     FS1        FS2        FS3        FS4
length     20     FS5        FS6        FS7        FS8
    ||     50     FS9        FS10       FS11       FS12
   
Input -
    roomLength, roomBreadth, numberOfHorizontalAirlifts, <Their Lengths>, numberOfVerticalAirlifts, <Their Lengths>
    100, 250, 2, 30, 50, 3, 20, 50, 100
'''

from itertools import product
import sys

(hallLength, hallBreadth, airliftDetails) = sys.argv[1].split(",", 2)
hallLength = int(hallLength)
hallBreadth = int(hallBreadth)
airliftDetails = list(map(int, airliftDetails.split(",")))

numberOfHorizontalAirlifts = airliftDetails[0]
numberOfVerticalAirlifts = airliftDetails[numberOfHorizontalAirlifts + 1]

print("-------------------------- Problem Statement1: Started -----------------------------------------")
#--------------------------------------------------------------------------------
# Function to find the lengths of individual blocks (roomlet) created by airlifts
#--------------------------------------------------------------------------------
def get_divisions(hallDimension, airliftDetails, startIndex, endIndex):
    divisions = list(map(int, []))
    previousLength = hallDimension
    for distance in reversed(airliftDetails[startIndex:endIndex]):
        # print(distance)
        divisions.append(previousLength - distance)
        previousLength = distance
        
    # Add the first airlift's dimension
    divisions.append(airliftDetails[startIndex] - 0)
    divisions = list(reversed(divisions))
    
    return(divisions)

#---------------------------------------------------------------------
# Find the lengths of individual blocks created by horizontal airlifts
#---------------------------------------------------------------------
lengthWiseDivisions = get_divisions(hallLength, airliftDetails, 1, numberOfHorizontalAirlifts + 1)
# print(lengthWiseDivisions)

#---------------------------------------------------------------------
# Find the breadths of individual blocks created by vertical airlifts
#----------------------------------------------------------------------
breadthWiseDivisions = get_divisions(hallBreadth, airliftDetails, numberOfHorizontalAirlifts + 2, numberOfHorizontalAirlifts + 2 + numberOfVerticalAirlifts + 1)
# print(breadthWiseDivisions)

#------------------------------------------------------------------------------------------
# Use the individual length-wise and breadth-wise divisions(roomlet) to map atomic functional spaces
#------------------------------------------------------------------------------------------
atomicFunctionalSpaceArea = {}
functionalSpaceIndex = 1
for length in lengthWiseDivisions:
    for breadth in breadthWiseDivisions:
        atomicFunctionalSpaceArea[functionalSpaceIndex] = length * breadth
        functionalSpaceIndex += 1

# print(functionalSpaceIndex)
numberOfAtomicFunctionalSpaces = functionalSpaceIndex - 1
# print(atomicFunctionalSpaceArea)

#-------------------------------------------------------------------------------------------
# Algo to find the adjacent atomic functional spaces
#-------------------------------------------------------------------------------------------
adjacencyList = {}
for functionalSpaceIndex in range(1, numberOfAtomicFunctionalSpaces + 1):
    # print(functionalSpaceIndex)
    adjacencyList[functionalSpaceIndex] = set()
   
    # North element
    if(1 <= functionalSpaceIndex - numberOfVerticalAirlifts - 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex - numberOfVerticalAirlifts - 1)
   
    # South element
    if(1 <= functionalSpaceIndex + numberOfVerticalAirlifts + 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex + numberOfVerticalAirlifts + 1)
   
    # East element
    if((functionalSpaceIndex - 1) % (numberOfVerticalAirlifts + 1) != 0 and 1 <= functionalSpaceIndex - 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex - 1)
        
    # West element
    if((functionalSpaceIndex + 1) % (numberOfVerticalAirlifts + 1) != 1 and 1 <= functionalSpaceIndex + 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex + 1)
   
# print(adjacencyList)

#------------------------------------------------------------------------------------------
# Function: Algo to find all functional spaces
#------------------------------------------------------------------------------------------
def dfs(graph, start, maxdegree, finalListOfFunctionalSpaces, path=None):
    if path is None:
        path = [start]
       
    if (maxdegree == 1):
        path.sort()
        if path not in finalListOfFunctionalSpaces:
            finalListOfFunctionalSpaces.append(path)
    else:
        for nextFS in graph[start] - set(path):
            if (maxdegree != 1):
                intermediatePath = path
                intermediatePath.sort()
                if intermediatePath not in finalListOfFunctionalSpaces:
                    finalListOfFunctionalSpaces.append(intermediatePath)
                dfs(graph, nextFS, maxdegree - 1, finalListOfFunctionalSpaces, path + [nextFS])

#------------------------------------------------------------------------------------------
# Algo to create all functional spaces
#------------------------------------------------------------------------------------------
finalListOfFunctionalSpaces = []
for i in range(1, numberOfAtomicFunctionalSpaces + 1):
        dfs(adjacencyList, i, numberOfAtomicFunctionalSpaces, finalListOfFunctionalSpaces)

# print(finalListOfFunctionalSpaces)

functionalSpaceAreas = {}
# FS functionalSpaceNumber comprises of atomic FS's listed in blocksList
for (functionalSpaceNumber, blocksList) in enumerate(finalListOfFunctionalSpaces):
    functionalSpaceAreas[functionalSpaceNumber] = sum(atomicFunctionalSpaceArea[x] for x in blocksList)
   
# print(functionalSpaceAreas)

#-------------------------------------------------------------------------------------------
# Problem Statement 2: Find the soultion to get the Functional Spaces for the requirement
#-------------------------------------------------------------------------------------------
print("---- Created Functional Spaces ----")
print("-------------------------- Problem Statement1: Ended -------------------------------------------")
print()
print("-------------------------- Problem Statement2: Started -----------------------------------------")
#--------------------------------------------------------------------------------------------
# Function: The allocation must be done in a way such that no two requests end up sharing the same space
#--------------------------------------------------------------------------------------------
def check_for_overlap(allocationBlocks):
    if(len(allocationBlocks) != len(set(allocationBlocks))):
        return False
    
    firstPossibleFunctionalSpaceNumber = allocationBlocks[0]
    previousFunctionalSpaceBlockList = set(finalListOfFunctionalSpaces[firstPossibleFunctionalSpaceNumber])
    
    for functionalSpaceNumber in allocationBlocks[1:]:
        # print(finalListOfFunctionalSpaces[previousFunctionalSpaceNumber])
        currentFunctionalSpaceBlockList = frozenset(finalListOfFunctionalSpaces[functionalSpaceNumber])
        if(not currentFunctionalSpaceBlockList.isdisjoint(previousFunctionalSpaceBlockList)):
            return False
        previousFunctionalSpaceBlockList = previousFunctionalSpaceBlockList.union(currentFunctionalSpaceBlockList)
   
    return True

#-------------------------------------------------------------------------------------------------
# Function: No functional space must be allocated to a request that is a superset for an existing allocation
#-------------------------------------------------------------------------------------------------
def is_not_a_superset(functionalSpaceNumber, spaceAllocation, currentRequestPossibleAllocations):
    atomicBlocksList = frozenset(finalListOfFunctionalSpaces[functionalSpaceNumber])
    
    for currentAllocation in currentRequestPossibleAllocations:
        currentAllocationBlocksList = frozenset(finalListOfFunctionalSpaces[currentAllocation])
        if(atomicBlocksList.issuperset(currentAllocationBlocksList)):
            break
    else:
        return True

#-----------------------------------------------------------------------------------------------
# Function: To generate the functional spaces as per the requirement
#-----------------------------------------------------------------------------------------------
def get_functional_space_allocation(requests, functionalSpaceAreas):
    spaceAllocation = []
    for requestedArea in requests:
        currentRequestPossibleAllocations = []
        for functionalSpaceNumber in functionalSpaceAreas:
            if(requestedArea <= functionalSpaceAreas[functionalSpaceNumber] and is_not_a_superset(functionalSpaceNumber, spaceAllocation, currentRequestPossibleAllocations)):
                currentRequestPossibleAllocations.append(functionalSpaceNumber)
        spaceAllocation.append(currentRequestPossibleAllocations)
        
    # print(spaceAllocation)    
   
    allPossibleFunctionalSpaceAllocations = []
    for allocationPossibility in filter(check_for_overlap, product(*spaceAllocation)):
        allPossibleFunctionalSpaceAllocations.append(allocationPossibility)               

    return(allPossibleFunctionalSpaceAllocations)

#-----------------------------------------------------------------------------------------------
# Function: To find the most efficient functional spaces for a given set of requirements
#-----------------------------------------------------------------------------------------------
def get_most_efficient_allocation(allPossibleFunctionalSpaceAllocations, numberOfSolutions=sys.maxsize):
    efficientAllocations = []
    
    # print(allPossibleFunctionalSpaceAllocations)
    
    allPossibleFunctionalSpaceAllocations.sort(key=lambda allocation: (sum(functionalSpaceAreas[fsNumber] for fsNumber in allocation), sum(len(finalListOfFunctionalSpaces[fsNumber]) for fsNumber in allocation)))
    
    #for allocation in allPossibleFunctionalSpaceAllocations:
        #print(allocation)
        # print([item for sublist in allocation for item in sublist])
        # print(sum(functionalSpaceAreas[fsNumber] for fsNumber in allocation), len(allocation))
        
    for allocation in allPossibleFunctionalSpaceAllocations:
        # efficientAllocations.append(allocation)
        # print(allocation)
        blocksList = []
        for fsAllocationPerRequest in allocation:
            blocksList.append(finalListOfFunctionalSpaces[fsAllocationPerRequest])
        efficientAllocations.append(blocksList)
        numberOfSolutions -= 1
        if(numberOfSolutions == 0):
            break
    
    return(efficientAllocations)

#-----------------------------------------------------------------------------------------------
# Function: To find the most efficient functional spaces for a given set of requirements
#-----------------------------------------------------------------------------------------------
def display_solutions(functionalSpaceAllocations):
    #print(functionalSpaceAllocations)
    for (solutionRank, allocation) in enumerate(functionalSpaceAllocations, 1):
        print("Solution", solutionRank, "-->")
        for (requestNumber, individualRequestAllocation) in enumerate(allocation, 1):
            print("Client request", requestNumber, " : ", end="")
            for atomicFunctionalSpace in individualRequestAllocation:
                print("Roomlet" + str(atomicFunctionalSpace), ' ', end="")
            print()
#-----------------------------------------------------------------------------------------------
# Get the number of request for particular day
#-----------------------------------------------------------------------------------------------
while(1):
    inputRequest = input("Number of requests hotel received for a particular day? (type: q for exit): ")
    if(inputRequest.lower() == 'q'): exit(0)
    
    requests = []
    count = 1
    
    for i in range(int(inputRequest)):
        print("Client %d requested for space in sqmt:" % (count))
        requests.append(int(input()))
        count = count + 1
        
    allPossibleFunctionalSpaceAllocations = get_functional_space_allocation(requests, functionalSpaceAreas)
    functionalSpaceAllocations = allPossibleFunctionalSpaceAllocations
    
    print("Which solution do you prefer to see?\n"
           "1. Top n efficient allocations\n"
           "2. All allocations")
    solutionSelect = input("Enter Option : ")
    numberOfSolutions = sys.maxsize
    if(solutionSelect == '1'):
        numberOfSolutions = int(input("Enter the number of solutions you wish to see : "))
    functionalSpaceAllocations = get_most_efficient_allocation(allPossibleFunctionalSpaceAllocations, numberOfSolutions)
    display_solutions(functionalSpaceAllocations)
print("-------------------------- Problem Statement2: Ended -----------------------------------------")
#-----------------------------END---------------------------------------
