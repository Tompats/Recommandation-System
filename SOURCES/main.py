import numpy as np
from os import path
from matrix import *
from avg import *
from sim import *
from interface import *
from execution import *




def writeResults(results,final_choice):
    print("Give name of the output file (as txt): ")
    filename = input()
    while(filename==""):
        print("Give name of the output file (as txt): ")
        filename = input()
    f = open(filename, "w")
    f.write('Results for: '+final_choice+'\n')
    f.write('Total Time: '+str(results[1])+'\n')
    f.write('Error RMSE: '+str(results[2])+'\n'+'Error PRE: '+str(results[3])+'\n')
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
        print('---SUCCESS!---\n---You can find the results in your file!---\nIf you wish to exit press e')
        e = input()
        if(e == 'e'):
            exit = True





if __name__ == '__main__':
    main()