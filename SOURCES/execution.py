import time
from filter import *
from sim import *
from error import *
from topk import *
from dict import *



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
    error_rmse = RMSE(rmse_array)
    error_pre = PRE(pre,k)
    end_time = time.time()
    total_time = end_time - start_time
    return [results,total_time,error_rmse,error_pre]