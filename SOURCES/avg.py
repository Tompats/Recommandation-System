def findUsersAverageScore(M_matrix):
    b_user = []
    for i in M_matrix:
        summ = 0
        counter = 0
        for j in i:
            if j!=0:
                summ+=j
                counter+=1
        avg = summ/counter
        b_user.append(avg)
    return b_user





def avgColumn(M_matrix,column):
    summ = 0
    counter = 0
    avg = 0
    for row in range(len(M_matrix)):
        x = M_matrix[row][column]
        if(x!=0):
            summ += x
            counter += 1
    if counter!=0:
        avg = summ / counter
    return avg






def findMoviesAverageScore(M_matrix):
    b_movie = []
    avg = 0
    for column in range(len(M_matrix[0])):
        avg = avgColumn(M_matrix,column)
        b_movie.append(avg)
    return b_movie








def avgScore(M_matrix):
    s = 0
    counter = 0
    for i in M_matrix:
        for j in i:
            if j!=0:
                s+=j
                counter+=1
    avg = s/counter
    return avg