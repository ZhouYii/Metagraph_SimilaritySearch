import numpy as np

def seed_matrix_AV(author, a_p, a_v, p_v) :
    venue_list = list(a_v[author])
    venue_index_map = dict()
    for i in enumerate(venue_list) :
        '''
            index[venue_name] = array_index
        '''
        venue_index_map[i[1]] = i[0]
    matrix = np.matrix([0]*len(venue_list))
    for p in a_p[author] :
        index = venue_index_map[p_v[p]]
        matrix[0, index] += 1
    return matrix, venue_index_map

def matrix_VP(venue_index_map, v_p) :
    venue_list = venue_index_map.keys()
    matrix_width = 0
    for v in venue_list :
        matrix_width += len(v_p[v])

    paper_index = dict()
    py_matrix = []
    zeros_prefix = 0
    for v in venue_list :
        row = [0]*zeros_prefix
        for p in v_p[v] :
            paper_index[p] = zeros_prefix
            zeros_prefix += 1
            row.append(1)
        row.extend([0]*(matrix_width - zeros_prefix))
        py_matrix.append(row)
    return np.matrix(py_matrix), paper_index

def matrix_PA(paper_index_map, p_a) :
    paper_list = paper_index_map.keys()
    author_index_map = dict()
    author_set = set()
    for p in paper_list :
        for a in p_a[p] :
            author_set.add(a)
    matrix_width = len(author_set)
    print "width" + str(matrix_width)

    for i in enumerate(author_set) :
        '''
            index[author_name] = arr_index
        '''
        author_index_map[i[1]] = i[0]

    py_matrix = []
    '''
        Each row is vector representing paper and authors.
        Order of rows must correspond to order of rows in the
        previous matrix.
    '''
    row_sequence = sorted(paper_index_map.items(), key = lambda x:x[1])
    for elem in row_sequence :
        print "row"+str(elem[1])
        row = [0] * matrix_width
        paper_id = elem[0]
        for author in p_a[paper_id] :
            row[author_index_map[author]] = 1
        py_matrix.append(row)

    return np.matrix(py_matrix), author_index_map

def candidates_APVPA(author, a_p, p_v, v_p, p_a) :
    venues = set()
    for p in a_p[author] :

        if not p_v.has_key(p) :
            continue

        venues.add(p_v[p])

    papers = set()
    for v in venues :

        for p in v_p[v] :
            if not p_v.has_key(p) :
                continue
            papers.add(p)

    candidates = set()
    for p in papers :
        if not p_a.has_key(p) :
            continue
        for a in p_a[p] :
            candidates.add(a)
    return candidates

def count_APVPA(start, end, a_p, p_v, v_p, p_a) :
    unique_venues = set()
    for p in a_p[start] :

        if not p_v.has_key(p) :
            continue

        unique_venues.add(p_v[p])

    unique_papers = set()
    for v in v_p.keys() :

        for p in v_p[v] :
            if not p_v.has_key(p) :
                continue
            unique_papers.add(p)

    papers_reaching_end = set([p for p in unique_papers if end in p_a[p]])
    venue_score = dict()
    for v in unique_venues :
        venue_score[v] = len(papers_reaching_end.intersection(v_p[v]))
    final_score = 0
    for p in a_p[start] :
        final_score += venue_score[p_v[p]]
    return final_score

def pathsim_APVPA(start, end, a_p, p_v, v_p, p_a, start_start = 0) :
    print "endpoint name ------> " + end

    '''
        Typically the A->A metapath count should be passed as parameter.
        Otherwise, it will be calculated for each candidate author.

        Generally, there should be an author-author score dictionary.
    '''
    if start_start == 0 :
        start_start = float(count_APVPA(start, start, a_p, p_v, v_p, p_a))
    print "start-start :"+str(start_start)
    start_end = float(count_APVPA(start, end, a_p, p_v, v_p, p_a))
    print "start-end :"+str(start_end)
    end_end = float(count_APVPA(end, end, a_p, p_v, v_p, p_a))
    print "end-end :"+str(end_end)

    if start_end < 0 :
       start_end *= -1

    return 2*start_end / (end_end + start_start)


