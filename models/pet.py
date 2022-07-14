class Pet:
    def __init__(self, document):
        for line in document:
            setattr(self, line, document[line])