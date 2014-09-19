'''
    Usage : 
    import build_hin
    p_a, p_p, p_v, a_p, v_p, a_v = build_hin.start()
'''

from tfidf import TFIDF

author_dict = dict()
coauthor_instances = dict()

input_file = open("publications.txt")
#input_file = open("pub_min.txt")
while True :
    '''
        Parse paper title.
        Test for EOF.
    '''
    line = input_file.readline().strip()
    if len(line) == 0 :
        break
    assert line[:2] == "#*"
    title = line[2:]

    '''
        Parse author.
    '''
    line = input_file.readline().strip()
    assert line[:2] == "#@"
    authors = [x for x in line[2:].split(',') if len(x) > 1]
    for a in authors :
        if not author_dict.has_key(a) :
            author_dict[a] = dict()
            coauthor_instances[a] = 0
        for b in authors :
            if a == b :
                continue
            if not author_dict[a].has_key(b) :
                author_dict[a][b] = 1
            else :
                author_dict[a][b] += 1
            coauthor_instances[a] += 1

    '''
        Parse Year
    '''
    input_file.readline()

    '''
        Parse Venue
    '''
    line = input_file.readline().strip()
    assert line[:2] == "#c"

    '''
        Parse paper id.
        Do not cast to integer. Simply unnecessary.
    '''
    line = input_file.readline().strip()
    assert line[:6] == "#index"

    '''
        Parse citations.
    '''
    line = input_file.readline().strip()
    while line[:2] == "#%" :
        '''
            Invalid/empty citation.
        '''
        if len(line) <= 2 :
            break
        line = input_file.readline().strip()

    '''
        Read the empty string line so the readline output is not confused with
        EOF.
        Sets the reading pointer to the next paper's title line.
    '''
    line = input_file.readline()
    if line[:2] == "#!" :
        input_file.readline()

output_file = open("coauthor_statistics.txt", "w")
for a in author_dict.keys() :
    if coauthor_instances[a] == 0 :
        '''
            No co-authors. 
        '''
        continue
    average_coauthored_papers = float(len(author_dict[a].keys())) / \
                                float(coauthor_instances[a])
    output_file.write("#"+ a + " average co-author count:" + \
                            str(average_coauthored_papers) + '\n')
    abv_average_coauthors = [x for x in author_dict[a].keys() \
                            if author_dict[a][x] > average_coauthored_papers]
    for b in abv_average_coauthors :
        output_file.write("\t" + b + " : " + str(author_dict[a][b]) + '\n')
output_file.close()
