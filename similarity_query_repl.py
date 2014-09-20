import math
'''
    Imports vectors of metagraph features in format (name, f1, f2, f3, f4).
    Init generates a list, sorted by sum of f1-f4.
    Queries will provide 4-tuple of feature scores and the search space is cut
    down to 0.1(sum of f1-f4) to 3(sum of f1-f4)
'''

def score_author(elem) :
    return elem[1] + elem[2] + elem[3] + elem[4]

def init(filepath) :
    author_list = []
    f = open(filepath)
    for line in f :
        vector = line.strip().split('\t')
        for int_index in range(1, len(vector)) :
            vector[int_index] = int(vector[int_index])
        author_list.append(tuple(vector))

    author_list = sorted(author_list, key = lambda x : x[1] + x[2] + x[3] + x[4])
    return author_list

def get_left_bound_index(author_list, target_value) :
    '''
        Author_list is sorted.
        Function returns two indicies to bound elements in the author list
        within some scalar window of target value.
    '''
    left_index_bound = 0
    right_index_bound = len(author_list) - 1

    '''
        Find lower bound index or nearest lesser value.
        Either lower_target includes the zero-th element (no separator between
        valid and invalid indicies) or there is some separator which we find by
        binary search.
    '''
    if target_value <= score_author(author_list[0]) :
        l_bound = 0
    else :
        while left_index_bound < right_index_bound :
            seek_index = (left_index_bound + right_index_bound) / 2
            elem_score = score_author(author_list[seek_index])
            if seek_index + 1 < len(author_list) :
                next_greatest = score_author(author_list[seek_index + 1])
                if elem_score == target_value or \
                        (elem_score < target_value and next_greatest >= target_value) :
                            l_bound = seek_index
                            break
            if target_value > score_author(author_list[seek_index]) :
                left_index_bound = seek_index
                continue
            else :
                right_index_bound = seek_index
                continue
    return l_bound

def get_right_bound_index(author_list, target_value) :
    '''
        Range search for upper bound
    '''
    left_index_bound = 0
    right_index_bound = len(author_list) - 1
    if target_value >= score_author(author_list[right_index_bound]) :
        r_bound = right_index_bound
    else :
        while left_index_bound < right_index_bound :
            seek_index = (left_index_bound + right_index_bound) / 2
            elem_score = score_author(author_list[seek_index])
            if seek_index - 1 >= 0 :
                prev_score = score_author(author_list[seek_index - 1])
                if prev_score < target_value and elem_score > target_value or \
                        elem_score == target_value :
                            r_bound = seek_index
                            break
            if target_value < elem_score :
                right_index_bound = seek_index
                continue
            else :
                left_index_bound = seek_index
                continue
    
    return r_bound

def cosine_similarity(elem1, elem2) :
    dot = 0
    euclid1 = 0
    euclid2 = 0
    for i in range(1,5) :
        '''
            Always normalize using first vector
        '''
        dot += float(elem2[i]) / float(elem1[i])
        euclid1 += 1
        euclid2 += math.pow((elem2[i] / float(elem1[i])), 2)

    if euclid1 == 0.0 or euclid2 == 0.0 :
        return 0

    return -1 * float(dot) / (math.sqrt(euclid1) * math.sqrt(float(euclid2)))

def euclidian_dist(elem1, elem2) :
    '''
        Normalized euclidian distance by first vector (elem1)
    '''
    accumulator = 0
    for dim in range(1, len(elem1)) :
        if float(elem1[dim]) == 0.0 :
            accumulator += math.pow(float(elem2[dim]), 2)
        else :
            accumulator += math.pow((1 - float(elem2[dim])/float(elem1[dim])), 2)
    return math.sqrt(accumulator)

def get_similar(author_list, elem) :
    '''
        Returns sub-list of author_list, sorted by cosine similarity.
        Input : Elem is in format (author_name, f1, f2, f3, f4)
    '''
    score = float(score_author(elem))
    upper_bound_index = get_right_bound_index(author_list, score * 3)
    lower_bound_index = get_left_bound_index(author_list, score * 0.1)
    sub_list = author_list[lower_bound_index:upper_bound_index + 1]
    return sorted(sub_list, key = lambda x: euclidian_dist(x, elem))

author_list = init("metagraph_feature_exploration")
output_file = open("similarity_scores_output.txt", "w")
elem = tuple("AnHai Doan
output_file.write("#" + str(elem[0]) + "\n")
res =  get_similar(author_list, elem)[:25]
for r in res : 
    output_file.write('\t' + str(r[0]) + " " + \
            "{0:.3f}".format(euclidian_dist(elem, r)) + '\n')

output_file.close()

