def binary_search(arr, key):
    mid= 0
    left= 0
    right= len(arr)-1
    step= 0
    while left<= right:
        step = step +1
        mid = (left + right)//2
        if (key== arr[mid]):
            return mid
        elif (key< arr[mid]):
            right= mid-1
        else:
            left= mid+1
    return -1
arr= [-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60]
key= 30
result= binary_search(arr, key)
print('vi tri thu i la', result)