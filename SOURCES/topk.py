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