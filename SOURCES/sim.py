import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds
from scipy import spatial



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