from pymongo import MongoClient

class Database:
    def __init__(self, mongo_url):
        self.client = MongoClient(mongo_url)
        self.db = self.client.chatpets
        self.users = self.db.users
        self.chats = self.db.chats
        self.globalchats = self.db.globalchats
        self.lost = self.db.lost
        self.chat_admins = self.db.chat_admins
        self.pay = self.db.pay
        self.donates = self.db.donates
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
        return self.chats.find_one({'id': chat_id})

    def get_chat(self, chat_id):
        return self.globalchats.find_one({'id': chat_id})

    def switch_pets(self, chat1, chat2):
        pet1 = self.get_pet(chat1)
        pet2 = self.get_pet(chat2)

        self.chats.update_one({'id': chat1}, {
            '$set': {'lvl': pet2['lvl'], 'hunger': pet2['hunger'], 'maxhunger': pet2['maxhunger'], 'exp': pet2['exp']}})
        self.chats.update_one({'id': chat2}, {
            '$set': {'lvl': pet1['lvl'], 'hunger': pet1['hunger'], 'maxhunger': pet1['maxhunger'], 'exp': pet1['exp']}})

    def choose_elites(self):
        self.users.update_many({}, {'$set': {'now_elite': False}})
        for elite in self.users.aggregate({'$sample': {'size': '10%'}}):
            self.users.update_one({'id': ids}, {'$set': {'now_elite': True}})

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

        
    def create_pet(self, chat_id):
        pet = self.form_pet(chat_id)
        self.chats.insert_one(pet)
    
    def createpet(id, typee='horse', name='Без имени'):
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
            'panda_feed': 0
        }