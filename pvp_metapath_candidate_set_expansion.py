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
paper_papers = dict()
paper_terms = dict()
term_papers = dict()
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

def start(tfidf_threshold) :

    #initialize TFIDF
    phrase_file = open("text_segmented_by_phrase.txt", "r")
    for line in phrase_file :
        index, text = line.split("##")
        token_list = text.lower().strip().split("!!")
        id_phrases[index] = token_list
    phrase_file.close()
    tfidf = TFIDF(id_phrases.values())
    print("TFIDF initialized")

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
            line = input_file.readline().strip()

        '''
            Read the empty string line so the readline output is not confused with
            EOF.
            Sets the reading pointer to the next paper's title line.
        '''
        line = input_file.readline()
        if line[:2] == "#!" :
            input_file.readline()

    '''
        Get terms for each paper.
    '''
    phrase_file = open("text_segmented_by_phrase.txt", "r")
    for paper_id, tok_list in id_phrases.items() :
        '''
            Assuming (id, list_of_tokens). If I'm wrong, the code will HCF.
        '''
        toks = [x for x in tok_list if len(x) > 2 and \
                                    tfidf.tf_idf(x) > tfidf_threshold]
        toks = sorted(toks, key=lambda x : tfidf.tf_idf(x), reverse = False)
        paper_terms[paper_id] = toks[: min(3, len(toks))]
        for term in paper_terms[paper_id] :
            if not term_papers.has_key(term) :
                term_papers[term] = []
            term_papers[term].append(paper_id)

    return paper_authors, \
           paper_papers, \
           paper_venue, \
           author_papers, \
           venue_papers, \
           author_venues

min_thresholds = [4,5,6,7,8,9,10]
for threshold_value in min_thresholds :
    output_file = open("candidate_expansion_metapath"+str(threshold_value), "w")
    start(threshold_value)
    for id, title in id_title.items() :
        printed_paper_ids = set()
        output_file.write("#" + str(title) + '\n')
        for term in paper_terms[id] :
            for paper_id in term_papers[term] :
                if paper_id in printed_paper_ids or not id_title.has_key(paper_id) :
                    continue
                printed_paper_ids.add(paper_id)
                output_file.write('\t' + id_title[paper_id] + " " + str(term) + '\n')

    output_file.close()


