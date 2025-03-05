myArray = [8,3,12,5,10]
print(myArray[3])
print(myArray[-2])
print(myArray.index(12))
#print(myArray[5])

def generateList():
    import random
    return [0, 1, 2, random.randrange(0, 10), 4]
def MinListNumGet(x: list[int]):
    lowest: int = x[0]
    for i in x:
        if i <= lowest:
            lowest = i
    if not lowest.is_integer:
        # Print an error
        print("error code L10-15")
    return lowest
def MaxListNumGet(y: list[int]):
    highest: int = y[0]
    for i in y:
        if i >= highest:
            highest = i
    return highest

numbers = generateList()
minNum = MinListNumGet(numbers)
MaxNum = MaxListNumGet(numbers)
print(f"The numbers are {numbers}\nThe Lowest {minNum}\nThe Highest {MaxNum}\n")

m = 5
for y in [1, 4, 2]:
    m = m - y
print(m)

    # to note that j is not an index
""" for j in numbers:
    print(numbers[j]) """ 
    
for index, value in enumerate(numbers):
    print(index, value)
    
textStr: str = "xYzAbC"
print(textStr)
print(textStr[1::2])
textStr = textStr[:2] + '\t' + textStr[2:]
print(textStr)
