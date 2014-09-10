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
