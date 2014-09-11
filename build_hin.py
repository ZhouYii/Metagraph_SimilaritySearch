'''
    Usage : 
    import build_hin
    p_a, p_p, p_v, a_p, v_p, a_v = build_hin.start()
'''

'''
    Define the one-to-many relations in network schema
'''
author_papers = dict()
paper_papers = dict()
paper_authors = dict()
venue_papers = dict()

'''
    Not a relation in DBLP network but useful for generating matrix
'''
author_venues = dict()

'''
    Define the one-to-one relations in network schema
'''
paper_venue = dict()

def dictionary_add_set(dictionary, key, value) :
    '''
        Add key-value pair to dictionary, where the collection type is set.
    '''
    if not dictionary.has_key(key) :
        dictionary[key] = set()
    dictionary[key].add(value)

def start() :

    input_file = open("publications.txt")
    while True :
        '''
            Parse paper title.
            Test for EOF.
        '''
        line = input_file.readline().strip()
        if len(line) == 0 :
            break
        assert line[:2] == "#*"

        '''
            Parse author.
        '''
        line = input_file.readline().strip()
        assert line[:2] == "#@"
        authors = line[2:].split(',')

        '''
            Parse Year
        '''
        input_file.readline()

        '''
            Parse Venue
        '''
        line = input_file.readline().strip()
        assert line[:2] == "#c"
        venue = line[2:]

        '''
            Parse paper id.
            Do not cast to integer. Simply unnecessary.
        '''
        line = input_file.readline().strip()
        assert line[:6] == "#index"
        id = line[6:]

        for a in authors :
            dictionary_add_set(author_papers, a, id)
            dictionary_add_set(author_venues, a, venue)
        dictionary_add_set(venue_papers, venue, id)

        paper_venue[id] = venue
        paper_authors[id] = authors

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
            dictionary_add_set(paper_papers, id, line[2:])
            line = input_file.readline().strip()

        '''
            Read the empty string line so the readline output is not confused with
            EOF.
            Sets the reading pointer to the next paper's title line.
        '''
        line = input_file.readline()
        if line[:2] == "#!" :
            input_file.readline()

    return paper_authors, \
           paper_papers, \
           paper_venue, \
           author_papers, \
           venue_papers, \
           author_venues
