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

def count_APVPA(start, end, a_p, p_v, v_p) :
    unique_venues = set()
    for p in a_p[author] :

        if not p_v.has_key(p) :
            continue

        unique_venues.add(p_v[p])

    unique_papers = set()
    for v in venues :

        for p in v_p[v] :
            if not p_v.has_key(p) :
                continue
            unique_papers.add(p)

    papers_reaching_end = set([p for p in unique_papers if end in p_a[p]])
    venue_score = dict()
    for v in unique_venues :
        venue_score[v] = papers_reaching_end.intersection(v_p[v])
    final_score = 0
    for p in a_p[start] :
        final_score += venue_score[p_v[p]]

    return final_score

def pathsim_APVPA(start, end, a_p, p_v, v_p) :
    start_start = float(count_AVPVA(start, start, a_p, p_v, v_p))
    start_end = float(count_AVPVA(start, end, a_p, p_v, v_p))
    end_end = float(count_AVPVA(end, end, a_p, p_v, v_p))

    if start_end < 0 :
       start_end *= -1

    return 2*start_end / (end_end + start_start)


