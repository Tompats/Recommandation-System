import math


def RMSE(array):
    summ = 0
    for pair in array:
        prediction = pair[0]
        real = pair[1]
        if(prediction>=0):
            summ += (prediction - real)**2
    error = math.sqrt(summ)
    return error





def PRE(pre_dict,k):
    array = []
    for user in pre_dict:
        arr = pre_dict[user]
        arr.sort()
        arr.reverse()
        if(len(arr)<k):
            k = len(arr)
        for i in range(0,k):
            array.append(arr[i])
    error = RMSE(array)
    return error