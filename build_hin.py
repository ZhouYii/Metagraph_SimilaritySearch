class HIN:
    def __init__(self, publications_file_path) :
        input_file = open(publications_file_path)
        self.papers = dict()
        self.authors = dict()
        self.venues = dict()
        for line in input_file :
            if line[:2] == "#*" :
                self.add_new_paper(input_file)

    def add_new_paper(self, input_file) :
        new_paper = Paper()
        line_count = 0
        for line in input_file :
            print "line:"+str(line_count)
            line_count += 1
            line = line.strip()
            '''
                End of data for one paper. Verify all fields are set and then
                add to the HIN database.
            '''
            if line[:2] == "#!" :
                if new_paper.verify_fields_are_set() :
                    self.papers[new_paper.id] = new_paper

                    for author in new_paper.get_authors() :
                        if not self.authors.has_key(author) :
                            self.authors[author] = set()
                        self.authors[author].add(new_paper)

                    if not self.venues.has_key(new_paper.get_venue()) :
                        self.venues[new_paper.get_venue()] = set()
                    self.venues[new_paper.get_venue()].add(new_paper)

            elif line[:2] == "#c" :
                new_paper.set_conference(line[2:])

            elif line[:2] == "#@" :
                new_paper.add_authors(line[2:].split(','))

            elif line[:2] == "#t" :
                new_paper.set_year(int(line[2:]))

            elif line[:2] == "#%" :
                if(len(line[2:]) > 0) :
                    new_paper.add_reference(int(line[2:]))

            elif line[:6] == "#index" :
                new_paper.set_self_id(int(line[6:]))

class Paper:
    def __init__(self) :
        self.reference_list = []
        self.authors = []
        self.year = None
        self.conference = None
        self.id = None

    def add_reference(self, reference_id) :
        self.reference_list.append(reference_id)

    def set_year(self, year) :
        self.year = year

    def set_self_id(self, self_id) :
        self.id = self_id

    def add_authors(self, author_list) :
        self.authors.extend(author_list)

    def set_conference(self, conference) :
        self.conference = conference

    def get_venue(self) :
        return self.conference

    def get_authors(self) :
        return self.authors

    def verify_fields_are_set(self) :
        if self.year == None or \
           self.id == None or \
           self.authors == [] or \
           self.conference == None :
                return False
        return True

print("Start")
hin = HIN("publications.txt")
