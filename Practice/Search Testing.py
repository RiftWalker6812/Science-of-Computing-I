

# Returns an Index of where the item is
def SeqSearch(arr, What_Im_Looking_For):
    for i in range(len(arr)):
        if arr[i] == What_Im_Looking_For:
            return i    # Return the index where it's found
    return -1    # Return -1 if not found

def BinarySearch(arr, What_Im_Looking_For):
    
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == What_Im_Looking_For:
            return mid
        elif arr[mid] < What_Im_Looking_For:
            left = mid + 1
        else:
            right = mid - 1
    return -1

words = sorted(["Apple", "Banana", "Cat", "Dog", "Elephant", "Fox", "Giraffe", "Horse", 
                "Iguana", "Jaguar", "Kangaroo", "Lion", "Monkey", "Nightingale", "Owl", 
                "Penguin", "Quail", "Rabbit", "Snake", "Tiger", "Unicorn", "Vulture", 
                "Wolf", "Xray", "Yak", "Zebra"])
target = "Tiger"

def printResult(i):
    if i == -1:
        return("Error")
    else:
        return(i)
        
import time
        
starttime = time.perf_counter()
result = SeqSearch(words, target)  
endtime = time.perf_counter()     

print(f"Seq Result, found {printResult(result)}, {(endtime-starttime):.9f}")
 
starttime = time.perf_counter()        
result = BinarySearch(words, target)
endtime = time.perf_counter()

print(f"Binary result, found {printResult(result)}, {(endtime-starttime):.9f}")