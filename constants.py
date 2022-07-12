ban = [96542998, 594119373, 820831937, -1001380240196]
totalban = [243153864, 866706209, 598442962, 765420407,
            786508668, 633357981, 521075049, 788297567, 709394939,
            638625062, 872696708, 941085059, 958911815, 579555709, 725226227, 594119373, 96542998,
            820831937, -1001380240196]
block = [-1001365421933, 725226227, 96542998, 820831937, -1001380240196]
PRIVATE = [-1001249266392]

INACTIVE_TIME = 60 * 60 * 24 * 14

alltypes = ['parrot', 'cat', 'dog', 'bear', 'pig', 'hedgehog', 'octopus', 'turtle', 'crab', 'spider', 'bee', 'owl',
                'boar', 'panda', 'cock', 'onehorn', 'goose', 'kaza']
cyber = 0

pet_abils = True
botname = 'Chatpetsbot'
admin_id = 792414733

def get_feed_text(pet):
    if pet['type'] == 'horse':
        spisok = ['яблоко', 'сено', 'хлеб', 'шоколадку', 'кукурузу', 'сахар', 'траву', 'рыбу', 'сосиску',
                    'макароны']
        s2 = ['немного металла', 'мышьяк', 'доску', 'хрен', 'сорняк', 'телефон', 'лошадь', 'автобус', 'компухтер',
                'карман']
        petname = 'Лошадь'
    if pet['type'] == 'cat':
        spisok = ['рыбу', 'мышь', 'кошачий корм', 'колбасу']
        s2 = ['миску', 'одеяло', 'шерсть']
        petname = 'Кот'
    if pet['type'] == 'parrot':
        spisok = ['траву', 'корм для попугая', 'орех', 'банан']
        s2 = ['телефон', 'клетку']
        petname = 'Попугай'
    if pet['type'] == 'dog':
        spisok = ['кость', 'корм для собак', 'куриную ножку', 'голубя']
        s2 = ['столб', 'мусорный бак', 'тетрадь']
        petname = 'Собака'
    if pet['type'] == 'bear':
        spisok = ['мёд', 'оленя', 'шишку']
        s2 = ['берлогу', 'горящую машину, а медведь сел в неё и сгорел', 'водку', 'балалайку']
        petname = 'Медведь'
    if pet['type'] == 'pig':
        spisok = ['корм для свиней', 'яблоко', 'гриб', 'белку']
        s2 = ['грязь', 'бриллианты']
        petname = 'Свинка'
    if pet['type'] == 'hedgehog':
        spisok = ['гриб', 'яблоко', 'жука', 'муравья']
        s2 = ['змею', 'стул', 'мяч']
        petname = 'Ёж'
    if pet['type'] == 'octopus':
        spisok = ['моллюска', 'улитку', 'рака', 'ската']
        s2 = ['банку с планктоном', 'корабль', 'сокровища']
        petname = 'Осьминог'
    if pet['type'] == 'turtle':
        spisok = ['капусту', 'яблоко', 'арбуз', 'дыню', 'хлеб']
        s2 = ['попугая', 'осьминога', 'карман']
        petname = 'Черепаха'
    if pet['type'] == 'crab':
        spisok = ['рыбий корм', 'морковь', 'перец', 'креветку', 'таракана', 'огурец']
        s2 = ['камень', 'крабовые чипсы']
        petname = 'Краб'
    if pet['type'] == 'spider':
        spisok = ['муху', 'стрекозу', 'кузнечика', 'попугая', 'жука']
        s2 = ['дом', 'слона']
        petname = 'Паук'
    if pet['type'] == 'bee':
        spisok = ['немного нектара', 'немного пыльцы', 'кусочек сахара']
        s2 = ['муравья', 'кита', 'цветок']
        petname = 'Пчела'
    if pet['type'] == 'owl':
        spisok = ['мышь', 'пчелу', 'рыбу', 'таракана']
        s2 = ['сову', 'компьютерную мышь', 'волка']
        petname = 'Сова'
    if pet['type'] == 'boar':
        spisok = ['орех', 'жёлудь']
        s2 = ['дерево', 'землю']
        petname = 'Кабан'
    if pet['type'] == 'panda':
        spisok = ['бамбук', 'большой бамбук', 'маленький бамбук', 'средний бамбук', 'яблоко', 'морковь', 'сосиску']
        s2 = ['лопату', 'не бамбук']
        petname = 'Панда'
    if pet['type'] == 'cock':
        spisok = ['зерно', 'лягушку', 'муху', 'муравья']
        s2 = ['доту', 'аниме', 'футбол', 'качалку', 'лигу легенд', 'hearthstone']
        petname = 'Петух'
    if pet['type'] == 'onehorn':
        spisok = ['радугу', 'сено', 'овёс', 'картошку']
        s2 = ['автобус', 'телефон', 'того, кто не верит в единорогов']
        petname = 'Единорог'
    if pet['type'] == 'goose':
        spisok = ['траву', 'зёрна', 'семена', 'клубнику', 'чернику']
        s2 = ['работягу', 'ЗАПУСКАЕМ ГУСЯ, РАБОТЯГИ', 'твич', 'Дуров, добавь эмодзи гуся в ТГ!']
        petname = 'Гусь'
    if pet['type'] == 'kaza':
        spisok = ['траву', 'яблоко']
        s2 = ['яблофон', 'резиновый мяч']
        petname = 'Коза'
    return spisok, s2, petname

pet_emojies = {
    'horse': '🐴',
    'parrot': '🦜',
    'cat': '🐱',
    'dog': '🐶',
    'octopus': '🐙',
    'turtle': '🐢',
    'hedgehog': '🦔',
    'pig': '🐷',
    'bear': '🐻',
    'crab': '🦀',
    'bee': '🐝',
    'spider': '🕷',
    'boar': '🐗',
    'owl': '🦉',
    'panda': '🐼',
    'cock': '🐓',
    'onehorn': '🦄',
    'goose': '🦆',
    'kaza': '🐐'
}

def pettoemoji(pet):
    return str(pet_emojies.get(pet))


def change_pet(pet):
    x = None
    pet = pet.lower()
    if pet == 'лошадь':
        x = 'horse'
    if pet == 'попугай':
        x = 'parrot'
    if pet == 'кот':
        x = 'cat'
    if pet == 'собака':
        x = 'dog'
    if pet == 'медведь':
        x = 'bear'
    if pet == 'свинка':
        x = 'pig'
    if pet == 'ёж':
        x = 'hedgehog'
    if pet == 'осьминог':
        x = 'octopus'
    if pet == 'черепаха':
        x = 'turtle'
    if pet == 'краб':
        x = 'crab'
    if pet == 'паук':
        x = 'spider'
    if pet == 'пчела':
        x = 'bee'
    if pet == 'сова':
        x = 'owl'
    if pet == 'кабан':
        x = 'boar'
    if pet == 'панда':
        x = 'panda'
    if pet == 'петух':
        x = 'cock'
    if pet == 'единорог':
        x = 'onehorn'
    if pet == 'гусь':
        x = 'goose'
    if pet == 'коза':
        x = 'kaza'
    return x

def pettype(pet):
    t = 'не определено'
    if pet == 'horse':
        return 'лошадь'
    if pet == 'parrot':
        return 'попугай'
    if pet == 'cat':
        return 'кот'
    if pet == 'dog':
        return 'собака'
    if pet == 'bear':
        return 'медведь'
    if pet == 'pig':
        return 'свинка'
    if pet == 'hedgehog':
        return 'ёж'
    if pet == 'octopus':
        return 'осьминог'
    if pet == 'turtle':
        return 'черепаха'
    if pet == 'crab':
        return 'краб'
    if pet == 'spider':
        return 'паук'
    if pet == 'bee':
        return 'пчела'
    if pet == 'owl':
        return 'сова'
    if pet == 'boar':
        return 'кабан'
    if pet == 'panda':
        return 'панда'
    if pet == 'cock':
        return 'петух'
    if pet == 'onehorn':
        return 'единорог'
    if pet == 'goose':
        return 'гусь'
    if pet == 'kaza':
        return 'коза'
    return t