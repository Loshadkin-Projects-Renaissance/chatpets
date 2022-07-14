from pymongo import MongoClient
from constants import *
import time
from models import User, Pet

class Database:
    def __init__(self, mongo_url):
        self.client = MongoClient(mongo_url)
        self.db = self.client.chatpets
        self.users = self.db.users
        self.chats = self.db.chats
        self.globalchats = self.db.globalchats
        self.lost = self.db.lost
        self.chat_admins = self.db.chat_admins
        self.curses = self.db.curseason

        self.initialization()

    def initialization(self):
        if not self.curses.find_one({}):
            self.curses.insert_one({
                'season': 15,
                'lastseason': 0

            })
        if not self.lost.find_one({'amount': {'$exists': True}}):
            self.lost.insert_one({'amount': 0})

    def get_pet(self, chat_id):
        pet = self.chats.find_one({'id': chat_id})
        if pet:
            return Pet(pet)

    def get_chat(self, chat_id):
        return self.globalchats.find_one({'id': chat_id})

    def get_user(self, user_id):
        user = self.users.find_one({'_id': user_id})
        if user:
            return User(user)

    def switch_pets(self, chat1, chat2):
        pet1 = self.get_pet(chat1)
        pet2 = self.get_pet(chat2)

        self.chats.update_one({'id': chat1}, {
            '$set': {'lvl': pet2['lvl'], 'hunger': pet2['hunger'], 'maxhunger': pet2['maxhunger'], 'exp': pet2['exp']}})
        self.chats.update_one({'id': chat2}, {
            '$set': {'lvl': pet1['lvl'], 'hunger': pet1['hunger'], 'maxhunger': pet1['maxhunger'], 'exp': pet1['exp']}})

    def user_cleanup(self):
        result = self.users.update_many({'time': {'$lt': time.time() - INACTIVE_TIME}}, {'$set': {'active': False}})
        return result.modified_count
    
    def chat_cleanup(self):
        result = self.globalchats.update_many({'time': {'$lt': time.time() - INACTIVE_TIME}}, {'$set': {'active': False}})
        return result.modified_count

    def choose_elites(self):
        self.users.update_many({}, {'$set': {ELITE: False}})
        size = self.users.count_documents({'active': True})
        print(f'Size: {size}')
        for elite in self.users.aggregate([{'$match': {'active': True}}, {'$sample': {'size': int(size/10)}}]):
            self.users.update_one({'_id': elite["_id"]}, {'$set': {ELITE: True}})

    def use_upgrade(self, chat_id):
        self.globalchats.update_one({'id': chat_id}, {'$set': {'new_season': False}})

        chat = self.get_chat(chat_id)

        lvl = 0

        for upgrade in [f'{i}_upgrade' for i in range(4)][::-1]:
            i = int(upgrade[0])
            if not i:
                upgrade = None
                break
            if chat[upgrade] > 0:
                lvl = 100*i
                break
                
        if upgrade:
            db.chats.update_one({'id': m.chat.id}, {
                '$set': {'lvl': lvl, 'maxhunger': 100 + lvl * 15, 'hunger': 100 + lvl * 15,
                            'exp': nextlvl({'lvl': lvl})}})
            db.globalchats.update_one({'id': m.chat.id}, {'$inc': {upg: -1}})

    def lose_horse(self, chat_id):  # returns True on success
        pet = self.chats.find_one({'id': chat_id})
        self.chats.delete_one({'id': chat_id})

        self.lost.insert_one(dict(pet))
        horse_id = self.lost.count_documents({'id': {'$exists': True}})
        while self.lost.find_one({'id': horse_id}) is not None:
            horse_id += 1
        self.lost.update_one({'id': chat_id}, {'$set': {'id': horse_id}})
        self.lost.update_one({'id': horse_id}, {'$set': {'type': 'horse'}})
        return True

    def give_pet(self, chat_id, pet):
        self.globalchats.update_one({'id': chat_id}, {'$inc': {'pet_access': -1}, '$addToSet': {'avalaible_pets': pet}})

    def take_horse(self, horse_id, new_chat_id):
        self.lost.update_one({'id': horse_id}, {'$set': {'id': new_chat_id}})
        pet = self.lost.find_one({'id': new_chat_id})
        self.lost.delete_one({'id': new_chat_id})
        self.chats.insert_one(pet)

    def create_pet(self, chat_id):
        pet = self.form_pet(chat_id)
        self.chats.insert_one(pet)

    def create_user(self, user):
        if self.get_user(user.id):
            return
        self.users.insert_one(self.from_user(user))

    def from_user(self, user):
        return {
            '_id': user.id,
            'name': user.first_name,
            'username': user.username,
            'active': True,
            'time': time.time(),
            ELITE: False
        }
    
    def form_pet(self, id, typee='horse', name='Без имени'):
        return {
            'id': id,
            'type': typee,
            'name': name,
            'lvl': 1,
            'exp': 0,
            'hp': 100,
            'maxhp': 100,
            'lastminutefeed': [],  # Список юзеров, которые проявляли актив в последнюю минуту
            'hunger': 100,
            'maxhunger': 100,
            'title': None,  # Имя чата
            'stats': {},  # Статы игроков: кто сколько кормит лошадь итд
            'spying': None,
            'send_lvlup': True,
            'lvlupers': [],
            'cock_check': 0,
            'panda_feed': 0,

            'active': True,
            'time': time.time()
        }

    def form_globalchat(self, id):
        return {
            'id': id,
            'avalaible_pets': ['horse'],
            'saved_pets': {},
            'pet_access': 0,
            'pet_maxlvl': 0,
            'achievements': [],
            '1_upgrade': 0,
            '2_upgrade': 0,
            '3_upgrade': 0,
            'new_season': False,
            'still': True
        }
