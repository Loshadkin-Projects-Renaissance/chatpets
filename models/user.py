from constants import *

class User:
    def __init__(self, document):
        self.id = document['_id']
        self.name = document['name']
        self.username = document['username']
        self.active = document['active']
        self.time = document['time']
        self.elite = document[ELITE]

    def to_dict(self):
        return {
            '_id': self.id,
            'name': self.name,
            'username': self.username,
            'active': self.active,
            'time': self.time,
            ELITE: self.elite
        }