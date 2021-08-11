import pandas as pd
from csv import reader
import time
from os import path
import math
import ast
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds
from scipy import spatial


#function for reading rating files and create appropriate dataframes
def ReadRatings(file):
    my_ratings_df = pd.read_csv(file)
    return my_ratings_df




def CreateUsersDictionary(my_ratings_df):
    copy_df = my_ratings_df.copy()
    unique_users = copy_df['userId'].unique()
    return unique_users


def CreateMoviesArray(my_ratings_df):
    copy_df = my_ratings_df.copy()
    unique_movies = copy_df['movieId'].unique()
    movies = list(unique_movies)
    return movies 




def create_A_matrix(movies_array,users_array,movies_dict,users_dict):
    A_matrix = []
    user_counter = -1
    for user in users_array:
        user_counter += 1
        users_dict[user] = user_counter
        row = []
        movie_counter = -1
        for movie in movies_array:
            if(user_counter==0):
                movie_counter +=1
                movies_dict[movie] = movie_counter
            row.append(0)  
        A_matrix.append(row)
    return A_matrix




def fill_A_matrix(A_matrix,movies_dict,file):
    with open(file, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                userID = int(row[0])
                movieID = int(row[1])
                rating = float(row[2])
                movie_pos = movies_dict[movieID]
                A_matrix[userID-1][movie_pos] = rating




def reverseDict(dictionary):
    reversed_dictionary = {value : key for (key, value) in dictionary.items()}
    return reversed_dictionary





def create_M_matrix(A_matrix,reversed_movies_dict,H_matrix):
    M_matrix = []
    
    for row in range(len(A_matrix)):
        record = []
        for column in range(len(A_matrix[row])):
            movieID = reversed_movies_dict[column]
            userID = row+1
            rating = A_matrix[row][column]
            if((movieID % 2 != 0) and (userID % 2 == 0) and rating!=0):
                record.append(0)
                H_matrix.append([row,column])
            else:
                record.append(rating)
        M_matrix.append(record)
    return M_matrix






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






def calculateSVD(M_matrix,d):
    svd_array = []
    temp_M = csc_matrix(M_matrix)
    U,s,Vt = svds(temp_M,d)
    S = np.diag(s)
    svd_array.append(U)
    svd_array.append(S)
    svd_array.append(Vt)
    return svd_array




def projectUsers(U_matrix,S_matrix,type):
    if(type=='a'):
        return U_matrix
    elif(type=='b'):
        S_sqrt = np.sqrt(S_matrix)
        result = np.matmul(U_matrix,S_matrix)
        return result





def projectMovies(V_matrix,S_matrix,type):
    if(type=='a'):
        return V_matrix
    elif(type=='b'):
        S_sqrt = np.sqrt(S_matrix)
        result = np.matmul(V_matrix,S_matrix)
        return result







#for movie give M_matrix transpose
def calculateNormp(M_matrix,object_avg):
    normp = {}
    for i in range(len(M_matrix)):
        normp[i] = [0]*len(M_matrix[i])
        for j in range(len(M_matrix[i])):
            if M_matrix[i][j] != 0:
                normp[i][j] = M_matrix[i][j] - object_avg[i]
    return normp



#for movie give M_matrix transpose
def calculatePearsonSim(M_matrix,object_normp,obj_pos):
    flag1 = False
    Pearson_Sim = {}
    if (max(object_normp[obj_pos])==0 and min(object_normp[obj_pos])==0):
        flag1 = True
    for j in range(len(M_matrix)):
        if(j!=obj_pos):
            flag2 = False
            if (max(object_normp[j])==0 and min(object_normp[j])==0):
                flag2 = True
            key = str(obj_pos) +',' + str(j)
            if(flag1 and flag2):
                Pearson_Sim[key] = 1
            elif(flag1 or flag2):
                Pearson_Sim[key] = 0
            else:
                Pearson_Sim[key] = 1 - spatial.distance.cosine(object_normp[obj_pos],object_normp[j])
    return Pearson_Sim





def calculateCosineSim(Rd,obj_pos):
    Cosine_Sim = {}
    flag1 = False
    if (max(Rd[obj_pos])==0 and min(Rd[obj_pos])==0):
        flag1 = True
    for j in range(len(Rd)):
        if(j!=obj_pos):
            flag2 = False
            if (max(Rd[j])==0 and min(Rd[j])==0):
                flag2 = True
            key = str(obj_pos) +',' + str(j)
            if(flag1 and flag2):
                Cosine_Sim[key] = 1
            elif(flag1 or flag2):
                Cosine_Sim[key] = 0
            else:
                Cosine_Sim[key] = 1 - spatial.distance.cosine(Rd[obj_pos],Rd[j])
    return Cosine_Sim





def sortDictByValue(dict):
    sort_list = sorted(dict.items(), key=lambda x: x[1])
    return sort_list



#for movie give M_matrix Transpose
def findTopK(k,Sim_sorted_list,M_matrix,obj_pos):
    topk = {}
    #reverse iteration
    i = len(Sim_sorted_list) - 1
    while i!= -1 and len(topk)!=k:
        key = Sim_sorted_list[i][0].split(',')
        new_key = int(key[1])
        if(M_matrix[new_key][obj_pos]!=0):
            rating = M_matrix[new_key][obj_pos]
            sim = Sim_sorted_list[i][1]
            topk[new_key] = [sim,rating]
        i-=1
    return topk
        







def UBCF_Weighted(topk_dict,b_users,b_movies,obj_pos,movie,m):
    a = 0.0
    b = 0.0
    for key in topk_dict:
        sim = topk_dict[key][0]
        rating = topk_dict[key][1]
        a += sim * (rating - (b_users[int(key)] + b_movies[movie] + m))
        b += sim
    if(b==0):
        a=0
        b=1
    prediction = (a/b) + b_users[obj_pos] + b_movies[movie] + m
    if(prediction>5):
        prediction = 5.0
    elif(prediction<0):
        prediction = 0.0
    return prediction






def UBCF_Uniform(topk_dict,b_users,b_movies,obj_pos,movie,m):
    a = 0.0
    b = []
    for key in topk_dict:
        sim = topk_dict[key][0]
        rating = topk_dict[key][1]
        a += (rating - (b_users[int(key)] + b_movies[movie] + m))
        b.append(rating)
    if(len(b)>0):
        len_b = len(b)
    else:
        len_b = 1
        a=0
    prediction = (a/len_b) + b_users[obj_pos] + b_movies[movie] + m
    if(prediction>5):
        prediction = 5.0
    elif(prediction<0):
        prediction = 0.0
    return prediction





def ΙBCF_Weighted(topk_dict,b_movies,b_users,obj_pos,user,m):
    a = 0.0
    b = 0.0
    for key in topk_dict:
        sim = topk_dict[key][0]
        rating = topk_dict[key][1]
        a += sim * (rating - (b_movies[int(key)] + b_users[user] + m))
        b += sim
    if(b==0):
        a=0
        b=1
    prediction = (a/b) + b_movies[obj_pos] + b_users[user] + m
    if(prediction>5):
        prediction = 5.0
    elif(prediction<0):
        prediction = 0.0
    return prediction






def ΙBCF_Uniform(topk_dict,b_movies,b_users,obj_pos,user,m):
    a = 0.0
    b = []
    for key in topk_dict:
        sim = topk_dict[key][0]
        rating = topk_dict[key][1]
        a += (rating - (b_movies[int(key)] + b_users[user] + m))
        b.append(rating)
    if(len(b)>0):
        len_b = len(b)
    else:
        a=0
        len_b = 1
    prediction = (a/len_b) + b_movies[obj_pos] + b_users[user] + m
    if(prediction>5):
        prediction = 5.0
    elif(prediction<0):
        prediction = 0.0
    return prediction






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






def setUI():
    choices = []
    pos_result = [['UBCF','ICBF','HYBRID'],['Pearson Similarity','Cosine Similarity from svd-a','Cosine Similarity from svd-b'],['Uniform','Weighted'],['RMSE','PRE']]
    print("***Filtering Algorithm***")
    print("----------------------------")
    print("1. UBCF")
    print("2. ICBF")
    print("3. HYBRID")
    print("----------------------------")
    print("Please choose one number: ")
    choice_filter = input()
    while(choice_filter not in ['1','2','3']):
        print("Please choose one number: ")
        choice_filter = input()
    choices.append(choice_filter)
    print("\n***Similarity Criterion***")
    print("----------------------------")
    print("1. Pearson Similarity")
    print("2. Cosine Similarity from svd-a")
    print("3. Cosine Similarity from svd-b")
    print("----------------------------")
    print("Please choose one number: ")
    choice_similarity = input()
    while(choice_similarity not in ['1','2','3']):
        print("Please choose one number: ")
        choice_similarity = input()
    choices.append(choice_similarity)
    print("\n***Rank Score Estimation***")
    print("----------------------------")
    print("1. Uniform")
    print("2. Weighted")
    print("----------------------------")
    print("Please choose one number: ")
    choice_estimation = input()
    while(choice_estimation not in ['1','2']):
        print("Please choose one number: ")
        choice_estimation = input()
    choices.append(choice_estimation)
    print("\n***Error Function***")
    print("----------------------------")
    print("1. RMSE")
    print("2. PRE")
    print("----------------------------")
    print("Please choose one number: ")
    choice_error = input()
    while(choice_error not in ['1','2']):
        print("Please choose one number: ")
        choice_error = input()
    choices.append(choice_error)
    print('\nRunning for: ')
    final = pos_result[0][int(choices[0])-1]+" Filtering with "+pos_result[1][int(choices[1])-1]+", "+pos_result[2][int(choices[2])-1]+" Estimation and "+pos_result[3][int(choices[3])-1]+" Error Function"
    print(final)
    return [choices,final]














def executeAlgorithms(choices,hidden,M_matrix,M_clone,k,user_normp,movie_normp,svda_users,svdb_users,svda_movies,svdb_movies,b_users,b_movies,reversed_movies_dict,A_matrix,m):
    #User filtering
    results = []
    rmse_array = []
    pre = {}
    start_time = time.time()
    if(choices[0]=='1'):
        for pair in hidden:
            user = pair[0]
            movie = pair[1]
            if(choices[1]=='1'):
                dict_user = calculatePearsonSim(M_matrix,user_normp,user)
            elif(choices[1]=='2'):
                dict_user = calculateCosineSim(svda_users,user)
            elif(choices[1]=='3'):
                dict_user = calculateCosineSim(svdb_users,user)
            sorted_dict = sortDictByValue(dict_user)
            topkd = findTopK(k,sorted_dict,M_matrix,movie)
            if(choices[2]=='1'):
                prediction = UBCF_Uniform(topkd,b_users,b_movies,user,movie,m)
            elif(choices[2]=='2'):
                prediction = UBCF_Weighted(topkd,b_users,b_movies,user,movie,m)
            real = A_matrix[user][movie]
            record = [user+1,reversed_movies_dict[movie],prediction,real]
            results.append(record)
            rmse_array.append([prediction,real])
            if user not in pre:
                pre[user] = [[prediction,real]]
            else:
                pre[user].append([prediction,real])
            
    #Item filtering
    if(choices[0]=='2'):
        for pair in hidden:
            user = pair[0]
            movie = pair[1]
            if(choices[1]=='1'):
                dict_movies = calculatePearsonSim(M_clone,movie_normp,movie)
            elif(choices[1]=='2'):
                dict_movies = calculateCosineSim(svda_movies,movie)
            elif(choices[1]=='3'):
                dict_movies = calculateCosineSim(svdb_movies,movie)
            sorted_dict = sortDictByValue(dict_movies)
            topkd = findTopK(k,sorted_dict,M_clone,user)
            if(choices[2]=='1'):
                prediction = ΙBCF_Uniform(topkd,b_movies,b_users,movie,user,m)
            elif(choices[2]=='2'):
                prediction = ΙBCF_Weighted(topkd,b_movies,b_users,movie,user,m)
            real = A_matrix[user][movie]
            record = [user+1,reversed_movies_dict[movie],prediction,real]
            results.append(record)
            rmse_array.append([prediction,real])
            if user not in pre:
                pre[user] = [[prediction,real]]
            else:
                pre[user].append([prediction,real])

    if(choices[0]=='3'):
        for pair in hidden:
            user = pair[0]
            movie = pair[1]
            if(choices[1]=='1'):
                dict_user = calculatePearsonSim(M_matrix,user_normp,user)
                dict_movies = calculatePearsonSim(M_clone,movie_normp,movie)
            elif(choices[1]=='2'):
                dict_user = calculateCosineSim(svda_users,user)
                dict_movies = calculateCosineSim(svda_movies,movie)
            elif(choices[1]=='3'):
                dict_user = calculateCosineSim(svdb_users,user)
                dict_movies = calculateCosineSim(svdb_movies,movie)
            sorted_dict_u = sortDictByValue(dict_user)
            sorted_dict_m = sortDictByValue(dict_movies)
            topkd_u = findTopK(k,sorted_dict_u,M_matrix,movie)
            topkd_m = findTopK(k,sorted_dict_m,M_clone,user)
            if(choices[2]=='1'):
                prediction_u = UBCF_Uniform(topkd_u,b_users,b_movies,user,movie,m)
                prediction_m = ΙBCF_Uniform(topkd_m,b_movies,b_users,movie,user,m)
            elif(choices[2]=='2'):
                prediction_u = UBCF_Weighted(topkd_u,b_users,b_movies,user,movie,m)
                prediction_m = ΙBCF_Weighted(topkd_m,b_movies,b_users,movie,user,m)
            prediction = 0.5*prediction_u + 0.5*prediction_m
            real = A_matrix[user][movie]
            record = [user+1,reversed_movies_dict[movie],prediction,real]
            results.append(record)
            rmse_array.append([prediction,real])
            if user not in pre:
                pre[user] = [[prediction,real]]
            else:
                pre[user].append([prediction,real])

    if(choices[3]=='1'):
        error = RMSE(rmse_array)
    else:
        error = PRE(pre,k)
    end_time = time.time()
    total_time = end_time - start_time
    return [results,total_time,error]












def writeResults(results,final_choice):
    print("Give name of the output file (as txt): ")
    filename = input()
    while(filename==""):
        print("Give name of the output file (as txt): ")
        filename = input()
    f = open(filename, "w")
    f.write('Results for: '+final_choice+'\n')
    f.write('Total Time: '+str(results[1])+'\n')
    f.write('Error: '+str(results[2])+'\n')
    f.write('\nUser,Movie,Prediction,Real Rating'+'\n')
    for i in results[0]:
        f.write(str(i)+'\n')
    f.close()






def main():
    print("WELCOME!\nBefore we can start please give me the ratings filename: ")
    filename = input()
    while(not path.exists(filename)):
        print("Invalid file. Try again: ")
        filename = input()
    print('\nPlease wait while i set everthing up...\n')
    ratings_df = ReadRatings(filename)
    movies_array = CreateMoviesArray(ratings_df)
    users_array = CreateUsersDictionary(ratings_df)
    users_dict = {}
    movies_dict = {}
    A_matrix = create_A_matrix(movies_array,users_array,movies_dict,users_dict)
    reversed_movies_dict = reverseDict(movies_dict)
    fill_A_matrix(A_matrix,movies_dict,filename)
    H_matrix = []
    M_matrix = create_M_matrix(A_matrix,reversed_movies_dict,H_matrix)
    avg_users = findUsersAverageScore(M_matrix)
    avg_movies = findMoviesAverageScore(M_matrix)
    m = avgScore(M_matrix)
    b_users = [x-m for x in avg_users]
    b_movies = [x-m for x in avg_movies]
    #print(b_user)
    svd = calculateSVD(M_matrix,3)
    U_matrix = svd[0]
    S_matrix = svd[1]
    V_matrix = svd[2].T
    svdb_users = projectUsers(U_matrix,S_matrix,'b')
    svdb_movies = projectMovies(V_matrix,S_matrix,'b')
    svda_users = projectUsers(U_matrix,S_matrix,'a')
    svda_movies = projectMovies(V_matrix,S_matrix,'a')
    #print(b_user[53])
    M_clone = np.array(M_matrix.copy()).T
    user_normp = calculateNormp(M_matrix,b_users)
    #M_clone = M_clone.T
    movie_normp = calculateNormp(M_clone,b_movies)
    k = 5
    exit = False
    while(not exit):
        t = setUI()
        choices = t[0]
        final_choice = t[1]
        results = executeAlgorithms(choices,H_matrix,M_matrix,M_clone,k,user_normp,movie_normp,svda_users,svdb_users,svda_movies,svdb_movies,b_users,b_movies,reversed_movies_dict,A_matrix,m)
        writeResults(results,final_choice)
        print('SUCCESS!\nYou can find the results in your file!\nIf you wish to exit press e')
        e = input()
        if(e == 'e'):
            exit = True





if __name__ == '__main__':
    main()