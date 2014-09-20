'''
    Usage : 
    import build_hin
    p_a, p_p, p_v, a_p, v_p, a_v = build_hin.start()
'''
from tfidf import TFIDF
from nltk import word_tokenize
'''
    Define the one-to-many relations in network schema
'''
id_title = dict()
id_phrases = dict()
author_papers = dict()

'''
    Current paper cites which other papers?
'''
paper_papers = dict()

'''
    Current paper is cited by which other papers?
'''
paper_incoming_edge_ids = dict()
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

def calculate_advisee_score(author_name, p_a, a_p, p_p) :
    if not a_p.has_key(author_name) :
        return 0
    '''
        Calculates coauthor-over-time graph metric.
    '''
    feature_count = 0
    '''
        A->P1
    '''
    papers = set(a_p[author_name])
    '''
        A->P1,P2 & P2->P1
    '''
    self_citing = [x for x in papers if p_p.has_key(x) and len(set(p_p[x]).intersection(papers)) > 0]
    for paper in self_citing :
        '''
            -1 because we do not count author_name from author list.
        '''
        feature_count += len(p_a[paper]) - 1
    return feature_count

def calculate_peer_outcitation_score(author_name, a_v, v_p, a_p, p_p_incoming) :
    '''
        Calculates the third metagraph feature score.
    '''
    structure_occurrence = 0
    papers = set(a_p[author_name])
    for venue in a_v[author_name] :
        if not v_p.has_key(venue) :
            continue
        candidates = set(v_p[venue])
        for paper_id in papers :
            if not p_p_incoming.has_key(paper_id) :
                continue
            citations = p_p_incoming[paper_id]
            common = citations.intersection(candidates)
            structure_occurrence += len(common)
    return structure_occurrence


def calculate_peer_incitation_score(author_name, a_v, v_p, a_p, p_p) :
    '''
        Calculates te second metagraph feature score.
    '''
    structure_occurrence = 0
    papers = set(a_p[author_name])
    for venue in a_v[author_name] :
        candidates = set(v_p[venue])
        for paper_id in candidates :
            if not p_p.has_key(paper_id) :
                continue
            citations = p_p[paper_id]
            common = papers.intersection(candidates)
            structure_occurrence += len(common)
    return structure_occurrence

def calculate_outside_venue_influence(author_name, a_p, p_v, p_p_incoming) :
    '''
        Calculates the first metagraph feature score.
    '''
    structure_occurrence = 0
    for id in a_p[author_name] :
        if not p_v.has_key(id) or not p_p_incoming.has_key(id) :
            continue
        invalid = p_v[id]
        out_venue_citations = [x for x in p_p_incoming[id] if p_v[x] != invalid]
        structure_occurrence += len(out_venue_citations)
    return structure_occurrence

def dictionary_add_set(dictionary, key, value) :
    '''
        Add key-value pair to dictionary, where the collection type is set.
    '''
    if not dictionary.has_key(key) :
        dictionary[key] = set()
    dictionary[key].add(value)

def start() :

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
        id_title[id] = title

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
            dictionary_add_set(paper_incoming_edge_ids, line[2:], id)
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

output_file = open("metagraph_feature_exploration", "w")
input_file = open("researchers", "r")
start()
for author_name in author_papers.keys() :
    ovi_score = calculate_outside_venue_influence(author_name, author_papers, \
            paper_venue, paper_incoming_edge_ids)
    peer_in = calculate_peer_incitation_score(author_name, author_venues, \
            venue_papers, author_papers, paper_papers)
    peer_out = calculate_peer_outcitation_score(author_name, author_venues, \
            venue_papers, author_papers, paper_papers)
    advisee = calculate_advisee_score(author_name, paper_authors, author_papers, paper_papers)
    output_file.write(str(author_name) + "\t" + str(ovi_score) + "\t" + \
            str(peer_in) + "\t" + str(peer_out) + "\t" + str(advisee) + "\n")
output_file.close()
