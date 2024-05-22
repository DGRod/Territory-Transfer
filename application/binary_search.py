
def binary_search(array, target):

    if len(array) <= 0:
        return None

    if array[0] is None:
        array.pop(0)

    index = len(array) // 2
    left = array[:index]
    right = array[index:]

    while left and right:
        if array[index][2] == target:
            #print("target found", array[index])
            return array[index]
        else:
            if array[index][2] > target:
                return binary_search(left, target)
            else:
                return binary_search(right, target)
    


    