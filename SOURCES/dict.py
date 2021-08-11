





def reverseDict(dictionary):
    reversed_dictionary = {value : key for (key, value) in dictionary.items()}
    return reversed_dictionary


def sortDictByValue(dictionary):
    sort_list = sorted(dictionary.items(), key=lambda x: x[1])
    return sort_list