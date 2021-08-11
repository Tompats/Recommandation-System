import pandas as pd
from csv import reader
from dict import *






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