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