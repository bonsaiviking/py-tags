#Generic tag library

class TagFile(object):
    def __init__(self):
        self.tags = {}
        self.files = {}

    def parse(self, f):
        raise NotImplementedError

    def parse_from_file(self, filename):
        with open(filename, "r") as f:
            self.parse(f)

class Tag(object):
    def __init__(self):
        self.name = None
        self.file = None
        self.text = None
        self.line = None
        self.byte = None
