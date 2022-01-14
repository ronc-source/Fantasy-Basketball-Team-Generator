#Merge sort algorithm to return a sorted 2D array
def playerMergeSort(playerArray):

    #Base Case
    if(len(playerArray) <= 1):
        return playerArray
    
    #Recursive case: divide the list into sub lists
    middle = len(playerArray) // 2

    left = playerArray[:middle]
    right = playerArray[middle:]

    #Recursively merge list into a sorted array
    return merge(playerMergeSort(left), playerMergeSort(right))
    

#return a sorted 2D array with the contents of the left and right array 
def merge(left, right):
    mergedArray = []
    leftPointer = rightPointer = 0

    #Set pointers to both the left and right array, assuming they are both sorted, compare and add to a return array
    while(leftPointer < len(left) and rightPointer < len(right)):
        if(left[leftPointer][-1] <= right[rightPointer][-1]):
            mergedArray.append(left[leftPointer])
            leftPointer += 1
        elif(right[rightPointer][-1] <= left[leftPointer][-1]):
            mergedArray.append(right[rightPointer])
            rightPointer += 1

    #For missing elements
    if(leftPointer < len(left)):
        for i in range(leftPointer, len(left)):
            mergedArray.append(left[i])
    
    if(rightPointer < len(right)):
        for i in range(rightPointer, len(right)):
            mergedArray.append(right[i])
    

    return mergedArray


#Return a reversed 2D array - parameter needs to be sorted prior to function call
def reverseArray(array):
    returnArray = []

    for i in range(len(array) - 1, -1, -1):
        returnArray.append(array[i])

    return returnArray


