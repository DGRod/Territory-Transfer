
def binary_search(array, target):

    if len(array) <= 0:
        return None

    if array[0] is None:
        array.pop(0)

    # Split the array into two sublists:
    index = len(array) // 2
    left = array[:index]
    right = array[index:]

    while left and right:
        # If the target address is found, return the associated item:
        if array[index][2] == target:
            #print("target found", array[index])
            return array[index]
        # Recursive call on whichever sublist contains the target:
        else:
            if array[index][2] > target:
                return binary_search(left, target)
            else:
                return binary_search(right, target)
    


    