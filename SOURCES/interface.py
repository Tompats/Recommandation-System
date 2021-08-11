def setUI():
    choices = []
    pos_result = [['UBCF','ICBF','HYBRID'],['Pearson Similarity','Cosine Similarity from svd-a','Cosine Similarity from svd-b'],['Uniform','Weighted']]
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
    print('\nRunning for: ')
    final = pos_result[0][int(choices[0])-1]+" Filtering with "+pos_result[1][int(choices[1])-1]+", "+pos_result[2][int(choices[2])-1]+" Estimation"
    print(final)
    return [choices,final]