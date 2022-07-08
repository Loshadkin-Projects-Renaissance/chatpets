# -*- coding: utf-8 -*-
from startup import *

bot.send_message(admin_id, 'Попітка встата!')

@bot.message_handler(func=lambda m: not is_actual(m))
def skip_message(m):
    pass

@bot.message_handler(commands=['switch_pets'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def switch_pets_handler(m):
    chat1 = int(m.text.split(' ')[1])
    chat2 = int(m.text.split(' ')[2])
    db.switch_pets(chat1, chat2)


@bot.message_handler(commands=['tell'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def tell_handler(m):
    tts = m.text.split(' ', 1)[1]
    wts = m.text.split(' ', 1)[0]
    bot.send_message(wts, tts)


@bot.message_handler(commands=['chatid'])
def chatid_handler(m):
    bot.send_message(m.chat.id, f'Айди чата: `{m.chat.id}`', parse_mode='Markdown')


@bot.message_handler(commands=['chat_amount'], func=admin_lambda)
def chat_amount_handler(m):
    bot.send_message(m.chat.id, f'Всего я знаю {db.chats.count_documents({})} чатов!')


@bot.message_handler(commands=['newses'], func=admin_lambda)
def newses_handler(m):
    db.globalchats.update_one({'id': m.chat.id}, {'$set': {'new_season': True}})
    bot.send_message(m.chat.id, 'Готово. В чате новый сезон.')


@bot.message_handler(commands=['testadd'], func=admin_lambda)
def addddd(m):
    db.globalchats.update_one({'id': m.chat.id}, {'$inc': {'1_upgrade': 1}})
    bot.send_message(m.chat.id, 'add1')

@bot.message_handler(commands=['newelite'], func=admin_lambda)
def elitecheckk(m):
    bot.reply_to(m, 'Начинаю перевыбор элиты.')
    choose_elites()
    bot.reply_to(m, 'Теоретически - готово.')


@bot.message_handler(commands=['getelite'], func=admin_lambda)
def elitecheckk(m):
    bot.reply_to(m, 'Произвожу поиск...')
    tts = ""
    for ids in db.users.find({'now_elite': True}):
        if not ids['now_elite']:
            continue
        if len(text) <= 2000:
            text += ids['name'] + '; '
        elif len(text2) <= 2000:
            text2 += ids['name'] + '; '
        else:
            text3 += ids['name'] + '; '
    try:
        bot.send_message(m.chat.id, text)
        bot.send_message(m.chat.id, text2)
        bot.send_message(m.chat.id, text3)
    except:
        pass


@bot.message_handler(commands=['elitecheck'], func=lambda m: admin_lambda(m) and reply_lambda(m))
def elitecheck_handler(m):
    user = db.users.find_one({'id': m.reply_to_message.from_user.id})
    if not user:
        return
    bot.send_message(m.chat.id, str(user['now_elite']))


@bot.message_handler(commands=['switch_lvlup'])
def switch_lvlup(m):
    try:
        chat = db.chats.find_one({'id': m.chat.id})
        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        if user.status == 'creator' or user.status == 'administrator' or m.from_user.id == m.chat.id or m.from_user.id == admin_id:
            if chat['send_lvlup']:
                db.chats.update_one({'id': m.chat.id}, {'$set': {'send_lvlup': False}})
                bot.send_message(m.chat.id, 'Теперь питомец *НЕ* будет присылать вам уведомления о повышении уровня!',
                                 parse_mode='markdown')
            else:
                db.chats.update_one({'id': m.chat.id}, {'$set': {'send_lvlup': True}})
                bot.send_message(m.chat.id, 'Теперь питомец будет присылать вам уведомления о повышении уровня!')

        else:
            if cyber != 1:
                bot.send_message(m.chat.id, 'Только администраторы чата могут делать это!')
            else:
                bot.send_message(m.chat.id, 'Только киберадминистраторы киберчата могут киберделать это!')

    except:
        pass


@bot.message_handler(commands=['cock'])
def cock_handler(m):
    x = db.users.find_one({'id': m.reply_to_message.from_user.id})
    if not x:
        bot.send_message(m.chat.id, 'Этого пользователя даже нет у меня в базе!')
    tts = f'Выбранный юзер сегодня{"" if x["now_elite"] else " НЕ"} элита!'
    bot.send_message(m.chat.id, tts, reply_to_message_id=m.message_id)
    db.chats.update_one({'id': m.chat.id}, {'$set': {'cock_check': time.time()}})


@bot.message_handler(commands=['showlvl'], func=lambda m: arguments_lambda(m) and admin_lambda(m))
def showlevel_handler(m):
    try:
        pet = {'lvl': int(m.text.split(' ')[1])}
        x = nextlvl(pet)
        bot.send_message(m.chat.id, str(x))
    except:
        pass


@bot.message_handler(commands=['donate'])
def donate(m):
    text = 'Для совершения добровольного пожертвования можно использовать сервис Донателло. ' + \
               'Ссылка: https://donatello.to/greatmultifandom\nЗаранее благодарим!'

    bot.send_message(m.chat.id, text, parse_mode='markdown')


@bot.message_handler(commands=['death'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def death_handler(m):
    chat = int(m.text.split(' ')[1])
    lvl = int(m.text.split(' ')[2])
    chatt = db.chats.find_one({'id': chat})
    db.chats.update_one({'id': chat}, {'$inc': {'lvl': lvl}})
    db.chats.update_one({'id': chat}, {'$set': {'exp': nextlvl(chatt)}})

    bot.send_message(m.chat.id, 'Операция выполнена. Чат получил (или потерял) ' + str(lvl) + ' уровней.')


@bot.message_handler(commands=['new_name'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def new_name_handler(m):
    chat_id = int(m.text.split(' ')[1])
    lvl = int(m.text.split(' ')[2])
    chatt = db.chats.find_one({'id': chat})
    db.chats.update_one({'id': chat}, {'$inc': {'lvl': lvl, 'exp': nextlvl(chatt)}})
    bot.send_message(m.chat.id, 'Операция выполнена. Чат получил (или потерял) ' + str(lvl) + ' уровней.')


@bot.message_handler(commands=['do'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def do_handler(m):
    try:
        x = m.text.split('/do ')[1]
        try:
            eval(x)
        except:
            bot.send_message(admin_id, traceback.format_exc())
    except:
        bot.send_message(admin_id, traceback.format_exc())


@bot.message_handler(commands=['growpet'])
def grow(m):
    if db.get_pet(m.chat.id):
        bot.send_message(m.chat.id, 'У вас уже есть лошадь!')
        return

    db.create_pet(m.chat.id)
    chat = db.globalchats.find_one({'id': m.chat.id})
    if not chat:
        return
    if not chat['new_season']:
        return

    lvl = 0
    upgrades = [f'{i}_upgrade' for i in range(4)]
    upgrades.reverse()
    for upgrade in upgrades:
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

    db.globalchats.update_one({'id': m.chat.id}, {'$set': {'new_season': False}})

    bot.send_message(m.chat.id, 'Поздравляю! Вы завели питомца (лошадь)! О том, как за ней ухаживать, можно прочитать в /help.')


@bot.message_handler(commands=['set_admin'], func=lambda m: creator_lambda(m) and reply_lambda(m, False))
def set_admin(m):
    chatt = db.chat_admins.find_one({'id': m.chat.id})
    if not chatt:
        db.chat_admins.insert_one(createchatadmins(m))
        chatt = db.chat_admins.find_one({'id': m.chat.id})
    if int(m.reply_to_message.from_user.id) not in chatt['admins']:
        db.chat_admins.update_one({'id': m.chat.id}, {'$push': {'admins': int(m.reply_to_message.from_user.id)}})
        bot.send_message(m.chat.id,
                                'Успешно установлен админ питомца: ' + m.reply_to_message.from_user.first_name)
    else:
        bot.send_message(m.chat.id, 'Этот юзер уже является администратором лошади!')



@bot.message_handler(commands=['remove_admin'], func=lambda m: creator_lambda(m) and reply_lambda(m, False))
def remove_admin(m):
    chatt = db.chat_admins.find_one({'id': m.chat.id})
    if chatt == None:
        db.chat_admins.insert_one(createchatadmins(m))
        chatt = db.chat_admins.find_one({'id': m.chat.id})
    if int(m.reply_to_message.from_user.id) in chatt['admins']:
        db.chat_admins.update_one({'id': m.chat.id}, {'$pull': {'admins': int(m.reply_to_message.from_user.id)}})
        bot.send_message(m.chat.id,
                            'Успешно удалён админ питомца: ' + m.reply_to_message.from_user.first_name + '.')
    else:
        bot.send_message(m.chat.id, 'Этот юзер не является администратором питомца!')


def createchatadmins(m):
    return {
        'id': m.chat.id,
        'admins': []
    }


@bot.message_handler(commands=['getids'], func=admin_lambda)
def idssssss(m):
    text = ''
    for h in db.lost.find({'id': {'$exists': True}}):
        text += str(h['id']) + ' ' + h['name'] + '\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['addkaza'], func=admin_lambda)
def addgoose(m):
    try:
        db.globalchats.update_one({'id': m.chat.id}, {'$push': {'avalaible_pets': 'kaza'}})
        bot.send_message(m.chat.id, 'Ура, коза')
    except:
        pass


@bot.message_handler(commands=['feed'])
def feeed(m):
    global cyber
    if m.text.lower() == '/feed' or m.text.lower() == '/feed@chatpetsbot':
        x = db.chats.find_one({'id': m.chat.id})
        if x is None:
            if cyber != 1:
                bot.send_message(m.chat.id, 'А кормить некого:(')
            else:
                bot.send_message(m.chat.id, 'А киберкормить некого:(')

            return
        petname = 'missingno'
        spisok = ['missingno']
        s2 = ['missingno']
        if x['type'] == 'horse':
            spisok = ['яблоко', 'сено', 'хлеб', 'шоколадку', 'кукурузу', 'сахар', 'траву', 'рыбу', 'сосиску',
                      'макароны']
            s2 = ['немного металла', 'мышьяк', 'доску', 'хрен', 'сорняк', 'телефон', 'лошадь', 'автобус', 'компухтер',
                  'карман']
            petname = 'Лошадь'
        if x['type'] == 'cat':
            spisok = ['рыбу', 'мышь', 'кошачий корм', 'колбасу']
            s2 = ['миску', 'одеяло', 'шерсть']
            petname = 'Кот'
        if x['type'] == 'parrot':
            spisok = ['траву', 'корм для попугая', 'орех', 'банан']
            s2 = ['телефон', 'клетку']
            petname = 'Попугай'
        if x['type'] == 'dog':
            spisok = ['кость', 'корм для собак', 'куриную ножку', 'голубя']
            s2 = ['столб', 'мусорный бак', 'тетрадь']
            petname = 'Собака'
        if x['type'] == 'bear':
            spisok = ['мёд', 'оленя', 'шишку']
            s2 = ['берлогу', 'горящую машину, а медведь сел в неё и сгорел', 'водку', 'балалайку']
            petname = 'Медведь'
        if x['type'] == 'pig':
            spisok = ['корм для свиней', 'яблоко', 'гриб', 'белку']
            s2 = ['грязь', 'бриллианты']
            petname = 'Свинка'
        if x['type'] == 'hedgehog':
            spisok = ['гриб', 'яблоко', 'жука', 'муравья']
            s2 = ['змею', 'стул', 'мяч']
            petname = 'Ёж'
        if x['type'] == 'octopus':
            spisok = ['моллюска', 'улитку', 'рака', 'ската']
            s2 = ['банку с планктоном', 'корабль', 'сокровища']
            petname = 'Осьминог'
        if x['type'] == 'turtle':
            spisok = ['капусту', 'яблоко', 'арбуз', 'дыню', 'хлеб']
            s2 = ['попугая', 'осьминога', 'карман']
            petname = 'Черепаха'
        if x['type'] == 'crab':
            spisok = ['рыбий корм', 'морковь', 'перец', 'креветку', 'таракана', 'огурец']
            s2 = ['камень', 'крабовые чипсы']
            petname = 'Краб'
        if x['type'] == 'spider':
            spisok = ['муху', 'стрекозу', 'кузнечика', 'попугая', 'жука']
            s2 = ['дом', 'слона']
            petname = 'Паук'
        if x['type'] == 'bee':
            spisok = ['немного нектара', 'немного пыльцы', 'кусочек сахара']
            s2 = ['муравья', 'кита', 'цветок']
            petname = 'Пчела'
        if x['type'] == 'owl':
            spisok = ['мышь', 'пчелу', 'рыбу', 'таракана']
            s2 = ['сову', 'компьютерную мышь', 'волка']
            petname = 'Сова'
        if x['type'] == 'boar':
            spisok = ['орех', 'жёлудь']
            s2 = ['дерево', 'землю']
            petname = 'Кабан'
        if x['type'] == 'panda':
            spisok = ['бамбук', 'большой бамбук', 'маленький бамбук', 'средний бамбук', 'яблоко', 'морковь', 'сосиску']
            s2 = ['лопату', 'не бамбук']
            petname = 'Панда'
        if x['type'] == 'cock':
            spisok = ['зерно', 'лягушку', 'муху', 'муравья']
            s2 = ['доту', 'аниме', 'футбол', 'качалку', 'лигу легенд', 'hearthstone']
            petname = 'Петух'
        if x['type'] == 'onehorn':
            spisok = ['радугу', 'сено', 'овёс', 'картошку']
            s2 = ['автобус', 'телефон', 'того, кто не верит в единорогов']
            petname = 'Единорог'
        if x['type'] == 'goose':
            spisok = ['траву', 'зёрна', 'семена', 'клубнику', 'чернику']
            s2 = ['работягу', 'ЗАПУСКАЕМ ГУСЯ, РАБОТЯГИ', 'твич', 'Дуров, добавь эмодзи гуся в ТГ!']
            petname = 'Гусь'
        if x['type'] == 'kaza':
            spisok = ['траву', 'яблоко']
            s2 = ['яблофон', 'резиновый мяч']
            petname = 'Коза'
        if random.randint(1, 100) <= 80:
            s = spisok
        else:
            s = s2
        word = random.choice(s)
        name = m.from_user.first_name
        name = name.replace('*', '\*').replace('_', '\_').replace("`", "\`")
        name2 = x['name'].replace('*', '\*').replace('_', '\_').replace("`", "\`")
        if cyber != 1:
            text = '' + name + ' достаёт из кармана *' + word + '* и кормит ' + name2 + '. ' + petname + ' с аппетитом съедает это!'
        else:
            text = 'Кибер' + name + ' достаёт из киберкармана *кибер' + word + '* и кормит Кибер' + name2 + '. Кибер' + petname + ' с кибераппетитом киберсъедает это!'

        bot.send_message(m.chat.id, text, parse_mode='markdown')


@bot.message_handler(commands=['commands'])
def commands(m):
    if cyber != 1:
        text = '/feed - покормить питомца (ни на что не влияет, просто прикол);\n'
        text += '/pogladit - погладить питомца\n'
        text += '/set_admin (только для создателя чата) - разрешить выбранному юзеру выгонять питомца из чата\n'
        text += '/remove_admin (только для создателя чата) - запретить юзеру выгонять питомца ' \
                '(только если ранее ему было это разрешено);\n'
        text += '/achievement_list - список ачивок, за которые можно получить кубы;\n'
        text += '/use_dice - попытка на получение нового типа питомцев;\n'
        text += '/select_pet pet - выбор типа питомца.\n'
        text += '@Chatpets - канал с обновлениями бота!'
    else:
        text = '/feed - покормить киберпитомца (ни на что не кибервлияет, просто киберприкол);\n'
        text += '/pogladit - погладить киберпитомца\n'
        text += '/set_admin (только для киберсоздателя киберчата) - киберразрешить выбранному киберюзеру выгонять ' \
                'киберпитомца из киберчата\n'
        text += '/remove_admin (только для киберсоздателя киберчата) - киберзапретить кибеоюзеру выгонять ' \
                'киберпитомца (только если киберранее ему было это киберразрешено);\n'
        text += '/achievement_list - список киберачивок, за которые можно киберполучить киберкубы;\n'
        text += '/use_dice - киберпопытка на киберполучение нового кибертипа киберпитомцев;\n'
        text += '/select_pet pet - выбор кибеотипа киберпитомца.\n'
        text += '@Chatpets - киберканал с киберобновлениями кибербота!'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['getpets'])
def getpet(m):
    if is_from_admin(m) or m.from_user.id == admin_id:
        db_pets = db.chats.find().sort('lvl', -1).limit(10)
        text = 'Топ-10 питомцев:\n\n'
        i = 1
        for doc in db_pets:
            text += str(i) + ' место: ' + make_safe_markdown(doc['name']) + ' (' + str(doc['lvl']) + ' лвл) (`' + str(
                doc['id']) + '`)' + '\n'
            i += 1
        try:
            bot.send_message(m.chat.id, text, parse_mode='markdown')
        except:
            bot.send_message(m.chat.id, text)


def make_safe_markdown(string):
    string = str(string)
    return string.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')


@bot.message_handler(commands=['rules'])
def rules(m):
    if cyber != 1:
        text = '1. Не использовать клиентских ботов для кормления питомца! За это будут наказания.\n' \
               '2. Не давать рекламу в списке выброшенных питомцев.'
    else:
        text = '1. Не использовать киберклиентских киберботов для киберкормления киберпитомца! ' \
               'За это будут кибернаказания.\n2. Не давать киберрекламу в киберсписке выброшенных киберпитомцев.'

    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['remove'])
def removee(m):
    if not is_from_admin(m):
        return
    try:
        db.lost.delete_one({'id': int(m.text.split(' ')[1])})
        bot.send_message(m.chat.id, "Питомец удален с улицы. НАВСЕГДА.")
    except:
        pass


@bot.message_handler(commands=['start'], func=lambda message: is_actual(message))
def startt(m):
    global cyber
    if m.from_user.id == m.chat.id:
        if cyber != 1:
            bot.send_message(m.chat.id, 'Здравствуй! /help для информации.')
        else:
            bot.send_message(m.chat.id, 'Киберздравствуй! /help для киберинформации.')


@bot.message_handler(commands=['info'])
def info(m):
    text = ''
    if not is_from_admin(m):
        return

    for ids in db.chats.find({}):
        text += str(ids) + '\n\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['top'], func=lambda message: is_actual(message))
def top(m):
    global cyber
    if m.text.lower() == '/top' or m.text.lower() == '/top@chatpetsbot':
        db_pets = db.chats.find().sort('lvl', -1).limit(10)
        if cyber != 1:
            text = 'Топ-10 питомцев:\n\n'
        else:
            text = 'Кибертоп-10 киберпитомцев:\n\n'

        i = 1
        for doc in db_pets:
            if cyber != 1:
                text += str(i) + ' место: ' + pettoemoji(doc['type']) + doc['name'].replace('\n', '') + ' (' + str(
                    doc['lvl']) + ' лвл)\n'
            else:
                text += str(i) + ' киберместо: ' + pettoemoji(doc['type']) + 'Кибер' + doc['name'] + ' (' + str(
                    doc['lvl']) + ' киберлвл)\n'

            i += 1

        bot.send_message(m.chat.id, text, disable_web_page_preview=True)


@bot.message_handler(commands=['help'], func=lambda message: is_actual(message))
def help(m):
    global cyber
    if m.text.lower() == '/help' or m.text.lower() == '/help@chatpetsbot':
        if cyber != 1:
            text = ''
            text += 'Чатовые питомцы питаются активностью юзеров. Чем больше вы общаетесь в чате, тем счастливее будет питомец! '
            text += 'Если долго не общаться, питомец начинает голодать и терять жизни. Назвать питомца можно командой /name\n'
            text += 'Для получения опыта необходимо иметь 85% сытости. Для получения бонусного опыта - 90% и 99% (за каждую отметку дается x опыта. То есть если у вас 90% сытости, вы получите (базовый_опыт + х), а если 99%, то (базовый_опыт + 2х).'
        else:
            text = ''
            text += 'Чатовые киберпитомцы питаются киберактивностью киберюзеров. Чем больше вы кибеообщаетесь в киберчате, тем киберсчастливее будет киберпитомец! '
            text += 'Если кибердолго не киберобщаться, киберпитомец начинает киберголодать и терять кибержизни. Киберназвать киберпитомца можно киберкомандой /name\n'
            text += 'Для получения киберопыта необходимо иметь 85% киберсытости. Для получения кибербонусного киберопыта - 90% и 99% (за каждую киберотметку дается x киберопыта. То есть если у вас 90% киберсытости, вы киберполучите (базовый_кибеоопыт + х), а если 99%, то (базовый_киберопыт + 2х).'

        bot.send_message(m.chat.id, text)


@bot.message_handler(func=lambda message: message.migrate_from_chat_id is not None, content_types=None)
def migrate(m):
    old_chat_id = m.migrate_from_chat_id
    new_chat_id = m.chat.id
    if db.chats.find_one({'id': old_chat_id}) is not None:
        db.chats.update_one({'id': old_chat_id}, {'$set': {'id': new_chat_id}})


@bot.message_handler(commands=['pogladit'])
def gladit(m):
    global cyber
    try:
        x = db.chats.find_one({'id': m.chat.id})
        if x is not None:
            if cyber != 1:
                bot.send_message(m.chat.id,
                                 m.from_user.first_name + ' погладил(а) ' + pettoemoji(x['type']) + x['name'] + '!')
            else:
                bot.send_message(m.chat.id, 'Кибер' + m.from_user.first_name + ' киберпогладил(а) ' + pettoemoji(
                    x['type']) + 'Кибер' + x['name'] + '!')

        else:
            if cyber != 1:
                bot.send_message(m.chat.id, 'А гладить некого!')
            else:
                bot.send_message(m.chat.id, 'А кибергладить кибернекого!')

    except:
        bot.send_message(admin_id, traceback.format_exc())


@bot.message_handler(commands=['achievement_list'])
def achlist(m):
    global cyber
    if cyber != 1:
        text = ''
        text += '1. За каждые 100 уровней даётся по 1 кубику, и так до 10000го.\n'
        text += '2. За сообщение от Дмитрия Исаева в вашем чате даётся 3 кубика!\n'
        text += '3. За актив в чате (сообщения от 10ти пользователей за минуту) даётся 3 кубика!\n'
        text += 'В будущем я добавлю секретные ачивки (но вам об этом не скажу)! Список ачивок будет пополняться.'
    else:
        text = ''
        text += '1. За каждые киберсто кибеоуровней даётся по 1 киберкубику, и так до кибердесятитысячногого.\n'
        text += '2. За киберсообщение от КиберДмитрия Исаева в вашем киберчате даётся 3 киберкубика!\n'
        text += '3. За киберактив в киберчате (киберсообщения от 10ти киберпользователей за киберминуту) даётся 3 киберкубика!\n'
        text += 'В кибербудущем я добавлю киберсекретные киберачивки (но вам об этом не киберскажу)! Киберсписок киберачивок будет киберпополняться.'

    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['addexp'])
def addexp(m):
    if is_from_admin(m):
        try:
            db.chats.update_one({'id': m.chat.id}, {'$inc': {'exp': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['addhunger'])
def addexp(m):
    if is_from_admin(m):
        try:
            db.chats.update_one({'id': m.chat.id},
                             {'$inc': {'maxhunger': int(m.text.split(' ')[1]), 'hunger': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['addlvl'])
def addlvl(m):
    if is_from_admin(m):
        try:
            db.chats.update_one({'id': m.chat.id}, {'$inc': {'lvl': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['reboot'])
def addlvl(m):
    if is_from_admin(m):
        try:
            db.chats.update_one({'id': m.chat.id}, {'$set': {'hunger': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['petstats'], func=lambda message: is_actual(message))
def petstats(m):
    global cyber
    animal = db.chats.find_one({'id': m.chat.id})
    if animal is None:
        bot.send_message(m.chat.id, 'Сначала питомца нужно завести (или подобрать с улицы).')
        return
    emoj = pettoemoji(animal['type'])
    if cyber != 1:
        text = ''
        text += emoj + 'Имя: ' + animal['name'] + '\n'
        text += '🏅Уровень: ' + str(animal['lvl']) + '\n'
        text += '🔥Опыт: ' + str(animal['exp']) + '/' + str(nextlvl(animal)) + '\n'
        text += '♥Здоровье: ' + str(animal['hp']) + '/' + str(animal['maxhp']) + '\n'
        p = int(animal['hunger'] / animal['maxhunger'] * 100)
        text += '🍔Сытость: ' + str(animal['hunger']) + '/' + str(animal['maxhunger']) + ' (' + str(p) + '%)' + '\n'
        text += 'Нужно сытости для постоянного получения опыта: ' + str(int(animal['maxhunger'] * 0.85))
    else:
        text = ''
        text += emoj + 'Киберимя: Кибер' + animal['name'] + '\n'
        text += '🏅Киберуровень: ' + str(animal['lvl']) + '\n'
        text += '🔥Киберопыт: ' + str(animal['exp']) + '/' + str(nextlvl(animal)) + '\n'
        text += '♥Киберздоровье: ' + str(animal['hp']) + '/' + str(animal['maxhp']) + '\n'
        p = int(animal['hunger'] / animal['maxhunger'] * 100)
        text += '🍔Киберсытость: ' + str(animal['hunger']) + '/' + str(animal['maxhunger']) + ' (' + str(
            p) + '%)' + '\n'
        text += 'Нужно киберсытости для киберпостоянного киберполучения киберопыта: ' + str(
            int(animal['maxhunger'] * 0.85))

    bot.send_message(m.chat.id, text)

"""

"""
@bot.message_handler(commands=['losthorses'], func=lambda message: is_actual(message))
def losthorses(m):
    global cyber
    if db.lost.count_documents({'id': {'$exists': True}}) == 0:
        if cyber != 1:
            bot.send_message(m.chat.id, "На улице питомцев нет!")
        else:
            bot.send_message(m.chat.id, "На киберулице киберпитомцев нет!")

        return
    if cyber != 1:
        text = 'Чтобы забрать питомца, введите команду /takeh id\n\n'
    else:
        text = 'Чтобы киберзабрать киберпитомца, кибервведите киберкоманду /takeh id\n\n'

    for pet in db.lost.find({'id': {'$exists': True}}):
        if cyber != 1:
            text += pettoemoji(pet['type']) + str(pet['id']) + ': ' + pet['name'] + " (" + str(
                pet['lvl']) + ' лвл)' + '\n'
        else:
            text += pettoemoji(pet['type']) + str(pet['id']) + ': Кибер' + pet['name'] + " (" + str(
                pet['lvl']) + ' киберлвл)' + '\n'

    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['takeh'], func=lambda message: is_actual(message))
def takeh(m):
    global cyber
    try:
        horse_id = int(m.text.split(' ')[1])
        if db.lost.find_one({'id': horse_id}) is None:
            if cyber != 1:
                bot.send_message(m.chat.id, "Питомец не существует!")
            else:
                bot.send_message(m.chat.id, "Киберпитомец не существует!")

            return

        if db.chats.find_one({'id': m.chat.id}) is not None:
            if cyber != 1:
                bot.send_message(m.chat.id, "У вас уже есть питомец!")
            else:
                bot.send_message(m.chat.id, "У вас уже есть киберпитомец!")

            return

        take_horse(horse_id, m.chat.id)
        db.chats.update_one({'id': horse_id}, {'$set': {'id': m.chat.id}})
        if cyber != 1:
            bot.send_message(m.chat.id,
                             "Поздравляем, вы спасли питомца от голода! Следите за ним, чтобы он рос и не голодал!")
        else:
            bot.send_message(m.chat.id,
                             "Киберпоздравляем, вы спасли киберпитомца от киберголода! Следите за ним, чтобы он киберрос и не киберголодал!")

    except:
        pass


def unban(id):
    try:
        ban.remove(id)
    except:
        pass


@bot.message_handler(commands=['getmsg'])
def getmsg(m):
    if m.from_user.id == admin_id:
        bot.send_message(admin_id, str(m.reply_to_message))


@bot.message_handler(commands=['throwh'], func=lambda message: is_actual(message))
def throwh(m):
    if m.chat.id not in ban:
        

        if db.chats.find_one({'id': m.chat.id}) is None:
            if cyber != 1:
                bot.send_message(m.chat.id, "У вас даже лошади нет, а вы ее выкидывать собрались!")
            else:
                bot.send_message(m.chat.id, "У вас даже киберлошади нет, а вы ее кибервыкидывать киберсобрались!")

            return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Подтверждаю.', callback_data='throwh ' + str(m.from_user.id)),
               types.InlineKeyboardButton(text='Отмена!', callback_data='cancel ' + str(m.from_user.id)))
        bot.send_message(m.chat.id, 'Подтвердите, что вы хотите выбросить лошадь.', reply_markup=kb)

    else:
        bot.send_message(m.chat.id, 'Выкидывать питомца можно только раз в час!')
        return


@bot.message_handler(commands=['ban'])
def bannn(m):
    if is_from_admin(m):
        try:
            totalban.append(int(m.text.split(' ')[1]))
            bot.send_message(m.chat.id, 'Бан.')
        except:
            pass


@bot.message_handler(commands=['name'], func=lambda message: is_actual(message))
def name(m):
    global cyber
    try:
        if m.chat.id in totalban or m.from_user.id in totalban:
            if cyber != 1:
                bot.send_message(m.chat.id,
                                 'Вам было запрещено менять имя питомца! Разбан через рандомное время (1 минута - 24 часа).')
            else:
                bot.send_message(m.chat.id,
                                 'Вам было киберзапрещено киберменять имя киберпитомца! Киберразбан через киберрандомное кибервремя (1 минута - 24 часа).')

            return

        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                m) and m.from_user.id != m.chat.id:
            if cyber != 1:
                bot.send_message(m.chat.id, 'Только админ может делать это!')
            else:
                bot.send_message(m.chat.id, 'Только киберадмин может киберделать это!')

            return

        name = m.text.split('/name ')[1]

        if db.chats.find_one({'id': m.chat.id}) is None:
            bot.send_message(m.chat.id, 'Для начала питомца нужно завести (/growpet)!')
            return

        if len(name) > 50:
            if cyber != 1:
                bot.send_message(m.chat.id, "Максимальная длина имени - 50 символов!")
            else:
                bot.send_message(m.chat.id, "Кибермаксимальная кибердлина киберимени - 50 киберсимволов!")

            return
        if len(name) < 2:
            if cyber != 1:
                bot.send_message(m.chat.id, "Минимальная длина имени - 2 символа!")
            else:
                bot.send_message(m.chat.id, "Киберминимальная кибердлина киберимени - 2 киберсимвола!")

            return
        db.chats.update_one({'id': m.chat.id}, {'$set': {'name': name}})
        try:
            bot.send_message(admin_id,
                             str(m.from_user.id) + ' ' + m.from_user.first_name + ' (имя: ' + name + ')')
        except:
            pass
        if cyber != 1:
            bot.send_message(m.chat.id, 'Вы успешно сменили имя питомца на ' + name + '!')
        else:
            bot.send_message(m.chat.id, 'Вы успешно киберсменили киберимя киберпитомца на Кибер' + name + '!')

    except:
        if cyber != 1:
            bot.send_message(m.chat.id,
                             'Для переименования используйте формат:\n/name *имя*\nГде *имя* - имя вашего питомца.',
                             parse_mode='markdown')
        else:
            bot.send_message(m.chat.id,
                             'Для киберпереименования используйте киберформат:\n/name *киберимя*\nГде *киберимя* - киберимя вашего киберпитомца.',
                             parse_mode='markdown')


@bot.message_handler(commands=['addcube'])
def addcubesss(m):
    if m.from_user.id != admin_id:
        return
    try:
        db.globalchats.update_one({'id': m.chat.id}, {'$inc': {'pet_access': int(m.text.split()[1])}})
        bot.send_message(m.chat.id, 'Успешно выдано ' + m.text.split()[1] + ' кубов!')
    except:
        bot.send_message(m.chat.id, 'Возможно, вы забыли указать количество. Хотя хз.')


@bot.message_handler(commands=['use_dice'])
def use_dice(m):
    global cyber
    alltypes = ['parrot', 'cat', 'dog', 'bear', 'pig', 'hedgehog', 'octopus', 'turtle', 'crab', 'spider', 'bee', 'owl',
                'boar', 'panda', 'cock', 'onehorn', 'goose', 'kaza']
    chat = db.globalchats.find_one({'id': m.chat.id})
    if not chat:
        return
    if chat['pet_access'] > 0:
        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                m) and m.from_user.id != m.chat.id:
            if cyber != 1:
                bot.send_message(m.chat.id, 'Только администратор может делать это!')
            else:
                bot.send_message(m.chat.id, 'Только киберадминистратор может киберделать это!')

            return
        tt = random.choice(alltypes)
        db.globalchats.update_one({'id': m.chat.id}, {'$inc': {'pet_access': -1}})
        if tt not in chat['avalaible_pets']:
            db.globalchats.update_one({'id': m.chat.id}, {'$push': {'avalaible_pets': tt}})
        if cyber != 1:
            bot.send_message(m.chat.id,
                             'Кручу-верчу, питомца выбрать хочу...\n...\n...\n...\n...\n...\nПоздравляю! Вам достался питомец "*' + pettype(
                                 tt) + '*"!', parse_mode='markdown')
        else:
            bot.send_message(m.chat.id,
                             'Киберкручу-киберверчу, киберпитомца выбрать хочу...\n...\n...\n...\n...\n...\nКиберпоздравляю! Вам достался киберпитомец "*кибер' + pettype(
                                 tt) + '*"!', parse_mode='markdown')

    else:
        if cyber != 1:
            bot.send_message(m.chat.id, 'У вас нет кубов! Зарабатывайте достижения для их получения!')
        else:
            bot.send_message(m.chat.id, 'У вас нет киберкубов! Зарабатывайте кибердостижения для их киберполучения!')


@bot.message_handler(commands=['chat_stats'])
def chatstats(m):
    x = db.globalchats.find_one({'id': m.chat.id})
    if not x:
        return
    pts = ''
    i = 1
    for ids in x['avalaible_pets']:
        if i != len(x['avalaible_pets']):
            pts += pettype(ids) + ', '
        else:
            pts += pettype(ids) + ';'
        i += 1
    lastpets = ''
    for ids in x['saved_pets']:
        hr = x['saved_pets'][ids]
        if cyber != 1:
            lastpets += pettoemoji(hr['type']) + hr['name'] + ': ' + str(hr['lvl']) + ' лвл\n'
        else:
            lastpets += pettoemoji(hr['type']) + 'Кибер' + hr['name'] + ': ' + str(hr['lvl']) + ' киберлвл\n'

    if cyber != 1:
        mult = 100
        try:
            for ids in x['saved_pets']:
                z = x['saved_pets'][ids]['lvl'] / 200
                if z > 0:
                    mult += z
            mult = round(mult, 2)
        except:
            print(traceback.format_exc())
        text = ''
        text += '➕Текущий бонус опыта за питомцев прошлых сезонов: ' + str(mult) + '%\n'
        text += 'Питомцы из прошлых сезонов: ' + lastpets + '\n'
        text += '🎖Максимальный уровень питомца в этом чате: ' + str(x['pet_maxlvl']) + ';\n'
        text += '🌏Доступные типы питомцев: ' + pts + '\n'
        text += '🎲Количество попыток для увеличения доступных типов (кубы): ' + str(
            x['pet_access']) + ' (использовать: /use_dice);\n'
        text += 'Малые усиления: ' + str(x['1_upgrade']) + ';\n'
        text += 'Средние усиления: ' + str(x['2_upgrade']) + ';\n'
        text += 'Большие усиления: ' + str(x['3_upgrade']) + '.'
    else:
        text = ''
        text += 'Киберпитомцы из прошлых киберсезонов: ' + lastpets + '\n'
        text += '🎖Кибермаксимальный киберуровень киберпитомца в этом киберчате: ' + str(x['pet_maxlvl']) + ';\n'
        text += '🌏Кибердоступные кибертипы киберпитомцев: ' + pts + '\n'
        text += '🎲Киберколичество киберпопыток для киберувеличения доступных кибертипов (киберкубы): ' + str(
            x['pet_access']) + ' (использовать: /use_dice).'
    try:
        bot.send_message(m.chat.id, text)
    except:
        bot.send_message(m.chat.id, 'Ошибка! Исправлю в ближайшее время.')
        bot.send_message(admin_id, traceback.format_exc())


@bot.message_handler(commands=['allinfo'])
def allinfo(m):
    if is_from_admin(m):
        text = str(db.chats.find_one({'id': m.chat.id}))
        bot.send_message(admin_id, text)


@bot.message_handler(commands=['igogo'])
def announce(m):
    if not is_from_admin(m):
        return

    text = m.text.replace('/igogo ', '', 1)
    chats_ids = db.chats.find({})
    i = 0
    for doc in chats_ids:
        try:
            bot.send_message(doc['id'], text)
            i += 1
        except:
            pass
    bot.send_message(m.chat.id, "Сообщение успешно получило " + str(i) + " чатиков")


@bot.message_handler(commands=['secret'])
def cubeee(m):
    chat = db.globalchats.find_one({'id': m.chat.id})
    if not chat:
        return
    if 'so easy' in chat['achievements']:
        return
    x = db.chats.find_one({'id': m.chat.id})
    if x != None:
        if x['lvl'] >= 15:
            db.globalchats.update_one({'id': m.chat.id},
                                   {'$push': {'a' + 'c' + 'h' + 'i' + 'evem' + 'ents': 'so easy'}})
            db.globalchats.update_one({'id': m.chat.id}, {'$inc': {'pet_access': 2}})
            if cyber != 1:
                bot.send_message(m.chat.id, 'Открыто достижение "Так просто?"! Награда: 2 куба.')
            else:
                bot.send_message(m.chat.id,
                                 'Открыто кибердостижение "Так киберпросто?"! Кибернаграда: 2 киберкуба.')

            bot.send_message(admin_id,
                             m.from_user.first_name + '(' + str(m.from_user.username) + ') открыл секрет!')
        else:
            if cyber != 1:
                bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')
            else:
                bot.send_message(m.chat.id,
                                 'Для кибероткрытия этого кибердостижения нужен минимум 15й киберуровень киберпитомца!')

    else:
        if cyber != 1:
            bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')
        else:
            bot.send_message(m.chat.id,
                             'Для кибероткрытия этого кибердостижения нужен минимум 15й киберуровень киберпитомца!')





def createuser(user):
    return {
        'id': user.id,
        'name': user.first_name,
        'username': user.username,
        'now_elite': False
    }
"""

"""

@bot.message_handler(commands=['select_pet'])
def selectpett(m):
    chat = db.globalchats.find_one({'id': m.chat.id})
    if not chat:
        return
    x = m.text.split(' ')
    if len(x) != 2:
        bot.send_message(m.chat.id,
                         'Ошибка! Используйте формат\n/select_pet pet\nГде pet - доступный вам тип питомцев (посмотреть их можно в /chat_stats).')
        return
    pet = x[1]
    newpet = change_pet(pet)
    if not newpet:
        return
    if not db.chats.find_one({'id': m.chat.id}):
        return
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(m) and m.from_user.id != m.chat.id:
        if cyber != 1:
            bot.send_message(m.chat.id, 'Только админ может делать это!')
        else:
            bot.send_message(m.chat.id, 'Только киберадмин может киберделать это!')

        return
    if newpet in chat['avalaible_pets']:
        db.chats.update_one({'id': m.chat.id}, {'$set': {'type': newpet}})
        if cyber != 1:
            bot.send_message(m.chat.id, 'Вы успешно сменили тип питомца на "' + pet + '"!')
        else:
            bot.send_message(m.chat.id,
                             'Вы киберуспешно сменили кибертип киберпитомца на "кибер' + pet + '"!')

    else:
        if cyber != 1:
            bot.send_message(m.chat.id, 'Вам сейчас не доступен этот тип питомцев!')
        else:
            bot.send_message(m.chat.id, 'Вам сейчас не кибердоступен этот кибертип киберпитомцев!')


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


def new_season(ses):
    bot.send_message(admin_id, 'Начинается новый сезон.')
    for ids in db.chats.find({}):
        x = db.globalchats.find_one({'id': ids['id']})
        if x == None:
            db.globalchats.insert_one(createglobalchat(ids['id']))
            x = db.globalchats.find_one({'id': ids['id']})
        db.globalchats.update_one({'id': ids['id']}, {'$set': {'saved_pets.' + str(ids['id']) + 'season' + str(ses): ids}})
        if ids['lvl'] > x['pet_maxlvl']:
            db.globalchats.update_one({'id': ids['id']}, {'$set': {'pet_maxlvl': ids['lvl']}})
    
    print('Second part of news.')
    db.globalchats.update_many({}, {'$set': {'new_season': True}})
    print(2.5)
    db_pets = db.chats.find().sort('lvl', -1).limit(10)
    print('Third part of news.')
    for doc in db_pets:
        db.globalchats.update_one({'id': doc['id']}, {'$inc': {'pet_access': 3}})
    print('Fourth part of news.')
    for ids in db.chats.find({}):
        try:
            bot.send_message(ids['id'],
                             'Начинается новый сезон! Все ваши текущие питомцы добавлены вам в дом, но кормить их больше не нужно, и уровень у них больше не поднимется. Они останутся у вас как память. Все чаты из топ-10 получают 3 куба в подарок!')
        except:
            pass
    db.chats.delete_many({})
    db.lost.delete_many({})
    bot.send_message(admin_id, 'Новый сезон начался!')


#@bot.message_handler(commands=['refresh_lvl'])
#def rrrlll(m):

    # if m.from_user.id==441399484:

    #   db.globalchats.update_many({},{'$set':{'avalaible_pets':['horse'], 'pet_access':2, 'achievements':[]}})


@bot.message_handler(content_types=['text'])
def messages(m):
    
    # if m.from_scheduled==True:
    #    bot.send_message(441399484,m.from_user.first_name+' ('+ str(m.from_user.username)+')\n'+m.text)
    #    return
    if random.randint(1, 100) <= 80:
        return
    if m.chat.id not in block:
        if db.users.find_one({'id': m.from_user.id}) == None:
            db.users.insert_one(createuser(m.from_user))
        if m.from_user.first_name == 'Telegram':
            pass  # bot.send_message(441399484, str(m.from_user))
        if db.globalchats.find_one({'id': m.chat.id}) == None:
            db.globalchats.insert_one(createglobalchat(m.chat.id))

        animal = db.chats.find_one({'id': m.chat.id})
        if animal is None:
            return
        lastminutefeed = animal['lastminutefeed']
        lvlupers = animal['lvlupers']
        title = animal['title']
        up = False
        if m.from_user.id not in animal['lastminutefeed']:
            lastminutefeed.append(m.from_user.id)
            up = True
        if m.from_user.id not in animal['lvlupers'] and db.users.find_one({'id': m.from_user.id})['now_elite'] == True:
            lvlupers.append(m.from_user.id)
            up = True
        if m.chat.title != animal['title']:
            title = m.chat.title
            up = True

        if up:
            db.chats.update_one({'id': m.chat.id},
                             {'$set': {'title': title, 'lvlupers': lvlupers, 'lastminutefeed': lastminutefeed}})



@bot.callback_query_handler(func=lambda call: True)
def calllsssff(call):
    if 'throwh' in call.data:
        global cyber
        if call.message.chat.id not in ban:
            user = bot.get_chat_member(call.message.chat.id, call.from_user.id)
            ch = db.chat_admins.find_one({'id': call.message.chat.id})
            if ch == None:
                if call.from_user.id != int(call.data.split(' ')[1]):
                    return
                if (
                        user.status != 'creator' and user.status != 'administrator') and call.from_user.id != call.message.chat.id:
                    medit('Только админ может делать это!', call.message.chat.id, call.message.message_id)
                    return
            else:
                if call.from_user.id not in ch['admins']:
                    if cyber != 1:
                        medit(
                            'Только админ питомца может делать это! Выставить админов может создатель чата по команде: /set_admin. Убрать админа можно командой /remove_admin.',
                            call.message.chat.id, call.message.message_id)
                    else:
                        pass
                    return

            if db.chats.find_one({'id': call.message.chat.id}) is None:
                if cyber != 1:
                    medit("У вас даже лошади нет, а вы ее выкидывать собрались!", call.message.chat.id,
                          call.message.message_id)
                else:
                    pass

                return

            if lose_horse(call.message.chat.id):
                ban.append(call.message.chat.id)
                t = threading.Timer(3600, unban, args=[call.message.chat.id])
                t.start()
                if cyber != 1:
                    medit("Вы выбросили питомца на улицу... Если его никто не подберет, он умрет от голода!",
                          call.message.chat.id, call.message.message_id)
                else:
                    pass

            else:
                medit(
                    "На улице гуляет слишком много лошадей, поэтому, как только вы ее выкинули, лошадь украли цыгане!",
                    call.message.chat.id, call.message.message_id)
        else:
            if cyber != 1:
                medit('Можно выгонять только одного питомца в час!', call.message.chat.id, call.message.message_id)
            else:
                pass

    elif 'cancel' in call.data:
        if call.from_user.id == int(call.data.split(' ')[1]):
            medit('Отменено.', call.message.chat.id, call.message.message_id)


def createglobalchat(id):
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
        'new_season': False
    }
    

def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)


def nextlvl(pet):
    return pet['lvl'] * (4 + pet['lvl'] * 100)


def check_hunger(pet, horse_lost):

    global cyber
    hunger = pet['hunger']
    maxhunger = pet['maxhunger']
    exp = pet['exp']
    lvl = pet['lvl']
    lastminutefeed = pet['lastminutefeed']
    global pet_abils
    if pet_abils == True:
        if pet['type'] == 'pig' and random.randint(1, 1000) <= 3:
            lvl += 1
            hunger += 15
            maxhunger += 15
            lvvl = lvl
            exp = nextlvl({'lvl': lvvl - 1})
            if pet['send_lvlup'] == True:
                try:
                    bot.send_message(pet['id'], 'Ваш питомец "свинка" повысил свой уровень на 1!')
                except:
                    pass
        if pet['type'] == 'panda' and hunger == maxhunger:
            db.chats.update_one({'id': pet['id']}, {'$inc': {'panda_feed': len(lastminutefeed) * 2}})
        if pet['type'] == 'panda' and hunger < maxhunger:
            addh = maxhunger - hunger
            if pet['panda_feed'] < addh:
                addh = pet['panda_feed']
            db.chats.update_one({'id': pet['id']}, {'$inc': {'panda_feed': -addh}})
            hunger += addh
        if pet['type'] == 'octopus' and hunger < maxhunger and random.randint(1, 100) <= 1:
            db_pets = db.chats.find().sort('lvl', -1).limit(10)
            try:
                trgt = random.choice(db_pets)
                if trgt['type'] == 'dog' and random.randint(1, 100) <= 30:
                    if trgt['send_lvlup'] == True:
                        bot.send_message(trgt['id'], 'Ваша собака спасла чат от осьминога "' + pet['name'] + '"!')
                    if pet['send_lvlup'] == True:
                        bot.send_message(pet['id'], 'Вашего осьминога прогнала собака "' + trgt['name'] + '"!')
                else:
                    colvo = int(pet['maxhunger'] * 0.01)
                    if colvo > int(trgt['maxhunger'] * 0.01):
                        colvo = int(trgt['maxhunger'] * 0.01)
                    db.chats.update_one({'id': trgt['id']}, {'$inc': {'hunger': -colvo}})
                    hunger += colvo
                    if trgt['send_lvlup'] == True:
                        bot.send_message(trgt['id'],
                                         'Осьминог "' + pet['name'] + '" украл у вас ' + str(colvo) + ' еды!')
                    if pet['send_lvlup'] == True:
                        bot.send_message(pet['id'],
                                         'Ваш осьминог украл у питомца "' + trgt['name'] + '" ' + str(colvo) + ' еды!')
            except:
                pass
        if pet['type'] == 'turtle' and random.randint(1, 1000) <= 3:
            db_pets = db.chats.find().sort('lvl', -1).limit(10)
            try:
                trgt = random.choice(db_pets)
                if trgt['type'] == 'dog' and random.randint(1, 100) <= 30:
                    if pet['send_lvlup'] == True:
                        try:
                            bot.send_message(pet['id'],
                                             'Ваш питомец "черепаха" попытался украсть уровень, но собака "' + trgt[
                                                 'name'] + '" прогнала вас!')
                        except:
                            pass
                    if trgt['send_lvlup'] == True:
                        try:
                            bot.send_message(trgt['id'],
                                             'Ваш питомец "собака" спас чат от черепахи "' + pet['name'] + '"!')
                        except:
                            pass
                else:
                    lvl += 1
                    hunger += 15
                    maxhunger += 15
                    lvvl = lvl
                    exp = nextlvl({'lvl': lvvl - 1})

                    db.chats.update_one({'id': trgt['id']}, {'$inc': {'lvl': -1, 'hunger': -15, 'maxhunger': -15}})
                    lvvl = db.chats.find_one({'id': trgt['id']})['lvl']
                    db.chats.update_one({'id': trgt['id']}, {'$set': {'exp': nextlvl({'lvl': lvvl - 1})}})
                    if pet['send_lvlup'] == True:
                        try:
                            bot.send_message(pet['id'],
                                             'Ваш питомец "черепаха" украл уровень у питомца "' + trgt['name'] + '"!')
                        except:
                            pass
                    if trgt['send_lvlup'] == True:
                        try:
                            bot.send_message(trgt['id'], 'Черепаха "' + pet['name'] + '" украла у вас 1 уровень!')
                        except:
                            pass


            except:
                pass

    # если кто-то писал в чат, прибавить кол-во еды равное кол-во покормивших в эту минуту * 2
    gchat = db.globalchats.find_one({'id': pet['id']})
    if gchat != None:
        if len(lastminutefeed) >= 10 and '10 db.users in one minute!' not in gchat['achievements']:
            db.globalchats.update_one({'id': pet['id']}, {'$push': {'achievements': '10 db.users in one minute!'}})
            db.globalchats.update_one({'id': pet['id']}, {'$inc': {'pet_access': 3}})
            if cyber != 1:
                bot.send_message(pet['id'], 'Заработано достижение: супер-актив! Получено: 3 куба (/chat_stats).')
            else:
                bot.send_message(pet['id'],
                                 'Заработано кибердостижение: кибер-супер-актив! Получено: 3 киберкуба (/chat_stats).')

    if gchat != None:
        if 86190439 in lastminutefeed and 'dmitriy isaev' not in gchat['achievements']:
            db.globalchats.update_one({'id': pet['id']}, {'$push': {'achievements': 'dmitriy isaev'}})
            db.globalchats.update_one({'id': pet['id']}, {'$inc': {'pet_access': 3}})
            if cyber != 1:
                bot.send_message(pet['id'], 'Заработано достижение: Дмитрий Исаев! Получено: 3 куба (/chat_stats).')
            else:
                bot.send_message(pet['id'],
                                 'Заработано кибердостижение: КиберДмитрий Исаев! Получено: 3 киберкуба (/chat_stats).')

    if len(lastminutefeed) > 0:
        hunger += len(lastminutefeed) * 10
        if pet_abils == True and pet['type'] == 'bear':
            hunger += len(lastminutefeed)
        lastminutefeed = []
        if hunger > maxhunger:
            hunger = maxhunger

    # если лошадь накормлена на 85% и выше, прибавить опыта
    h = hunger / maxhunger * 100
    bexp = 0
    if h >= 85:
        bexp += int(lvl * (2 + (random.randint(-100, 100) / 100)))
    if h >= 90:
        bexp += lvl
    if h >= 99:
        bexp += lvl
    mult = 100
    z = db.globalchats.find_one({'id': pet['id']})
    if z != None:
        try:
            for ids in z['saved_pets']:
                x = z['saved_pets'][ids]['lvl'] / 200
                if x > 0:
                    mult += x
            mult = mult / 100
            bexp = bexp * mult
        except:
            print(traceback.format_exc())
    exp += bexp
    if exp >= nextlvl(pet):
        lvl += 1
        maxhunger += 15
        if not horse_lost:
            if cyber != 1:
                send_message(pet['id'], 'Уровень вашего питомца повышен! Максимальный запас сытости увеличен на 15!',
                             act='lvlup')
            else:
                send_message(pet['id'],
                             'Киберуровень вашего киберпитомца повышен! Максимальный киберзапас киберсытости киберувеличен на 15!',
                             act='lvlup')

    ii = 100
    if gchat != None:
        while ii <= 10000:
            if lvl >= ii and 'lvl ' + str(ii) not in gchat['achievements']:
                db.globalchats.update_one({'id': pet['id']}, {'$push': {'achievements': 'lvl ' + str(ii)}})
                db.globalchats.update_one({'id': pet['id']}, {'$inc': {'pet_access': 1}})
                if cyber != 1:
                    bot.send_message(pet['id'],
                                     'Заработано достижение: ' + str(ii) + ' лвл! Получено: 1 куб (/chat_stats).')
                else:
                    bot.send_message(pet['id'], 'Заработано кибердостижение: ' + str(
                        ii) + ' киберлвл! Получено: 1 киберкуб (/chat_stats).')

            ii += 100

    commit = {'hunger': hunger, 'maxhunger': maxhunger, 'exp': int(exp), 'lvl': lvl, 'lastminutefeed': lastminutefeed}
    if not horse_lost:
        db.chats.update_one({'id': pet['id']}, {'$set': commit})
    else:
        db.lost.update_one({'id': pet['id']}, {'$set': commit})


def check_hp(pet, horse_lost):
    global cyber
    global pet_abils
    notlost = False
    if pet_abils == True:
        if pet['type'] == 'parrot' and random.randint(1, 100) <= 20:
            notlost = True
    if notlost == False:
        hunger = pet['hunger'] - random.randint(3, 9)
    else:
        hunger = pet['hunger']
    maxhunger = pet['maxhunger']  # const
    hp = pet['hp']
    maxhp = pet['maxhp']  # const

    if hunger <= 0:
        hunger = 0
        if not horse_lost:
            if cyber != 1:
                send_message(pet['id'], 'Ваш питомец СИЛЬНО голодает! Осталось ' + str(
                    hunger) + ' сытости! СРОЧНО нужен актив в чат!')
            else:
                send_message(pet['id'], 'Ваш киберпитомец КИБЕРСИЛЬНО киберголодает! Осталось ' + str(
                    hunger) + ' киберсытости! КИБЕРСРОЧНО нужен киберактив в киберчат!')

        hp -= random.randint(1, 2)

    elif hunger / maxhunger * 100 <= 30:
        if not horse_lost:
            if cyber != 1:
                send_message(pet['id'], 'Ваш питомец голодает! Осталось всего ' + str(
                    hunger) + ' сытости! Срочно нужен актив в чат!')
            else:
                send_message(pet['id'], 'Ваш киберпитомец киберголодает! Осталось всего ' + str(
                    hunger) + ' киберсытости! Киберсрочно нужен киберактив в киберчат!')

        hp -= random.randint(0, 1)

    elif hunger / maxhunger * 100 >= 75 and hp < maxhp:
        hp += random.randint(3, 9)
        if hp > maxhp:
            hp = maxhp

    if hp <= 0:
        total = db.lost.find_one({'amount': {'$exists': True}})['amount']
        total += 1
        db.lost.update_one({'amount': {'$exists': True}}, {'$inc': {'amount': 1}})
        if not horse_lost:
            db.chats.delete_one({'id': pet['id']})
            try:
                if cyber != 1:
                    bot.send_message(pet['id'],
                                     'Вашему питомцу плохо в вашем чате, ему не хватает питания. Поэтому я забираю его, чтобы он не умер.\n' +
                                     'Количество питомцев, которых мне пришлось забрать (во всех чатах): ' + str(total))
                else:
                    bot.send_message(pet['id'],
                                     'Вашему киберпитомцу киберплохо в вашем киберчате, ему не хватает киберпитания. Поэтому я киберзабираю его, чтобы он не киберумер.\n' +
                                     'Киберколичество киберпитомцев, которых мне пришлось киберзабрать (во всех киберчатах): ' + str(
                                         total))

            except:
                pass
        else:
            db.lost.delete_one({'id': pet['id']})

    else:
        commit = {'hunger': hunger, 'hp': hp}
        if not horse_lost:
            db.chats.update_one({'id': pet['id']}, {'$set': commit})
        else:
            db.lost.update_one({'id': pet['id']}, {'$set': commit})


def check_all_pets_hunger():
    threading.Timer(61, check_all_pets_hunger).start()

    for pet in db.lost.find({'id': {'$exists': True}}):
        check_hunger(pet, True)
    for pet in db.chats.find({}):
        check_hunger(pet, False)


def check_all_pets_lvlup():
    threading.Timer(1800, check_all_pets_lvlup).start()
    for pet in db.chats.find({}):
        check_lvlup(pet)
    db.chats.update_many({}, {'$set': {'lvlupers': []}})


def check_all_pets_hp():
    for pet in db.lost.find({'id': {'$exists': True}}):
        check_hp(pet, True)
    for pet in db.chats.find({}):
        check_hp(pet, False)
    threading.Timer(1800, check_all_pets_hp).start()

"""

"""
def check_lvlup(pet):
    global cyber
    lvl = 0
    for ids in pet['lvlupers']:
        lvl += 1
    if lvl > 0:
        #    if pet['lvl']>=10:
        db.chats.update_one({'id': pet['id']}, {'$inc': {'lvl': lvl, 'maxhunger': lvl * 15, 'hunger': lvl * 15}})
        lvvl = db.chats.find_one({'id': pet['id']})['lvl']

        db.chats.update_one({'id': pet['id']}, {'$set': {'exp': nextlvl({'lvl': lvvl - 1})}})
        if pet['send_lvlup'] == True:
            try:
                if cyber != 1:
                    bot.send_message(pet['id'],
                                     '"Друзья животных" в вашем чате подняли уровень питомца на ' + str(lvl) + '!')
                else:
                    bot.send_message(pet['id'],
                                     '"Кибердрузья киберживотных" в вашем киберчате подняли киберуровень киберпитомца на ' + str(
                                         lvl) + '!')

            except:
                pass


def pettoemoji(pet):
    if pet == 'horse':
        return '🐴'
    if pet == 'parrot':
        return '🦜'
    if pet == 'cat':
        return '🐱'
    if pet == 'dog':
        return '🐶'
    if pet == 'octopus':
        return '🐙'
    if pet == 'turtle':
        return '🐢'
    if pet == 'hedgehog':
        return '🦔'
    if pet == 'pig':
        return '🐷'
    if pet == 'bear':
        return '🐻'
    if pet == 'crab':
        return '🦀'
    if pet == 'bee':
        return '🐝'
    if pet == 'spider':
        return '🕷'
    if pet == 'boar':
        return '🐗'
    if pet == 'owl':
        return '🦉'
    if pet == 'panda':
        return '🐼'
    if pet == 'cock':
        return '🐓'
    if pet == 'onehorn':
        return '🦄'
    if pet == 'goose':
        return '🦆'
    if pet == 'kaza':
        return '🐐'


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


def send_message(chat_id, text, act=None):  # использовать только чтобы проверить что лошадь все еще в чате
    h = db.chats.find_one({'id': chat_id})
    try:
        if act == None:
            bot.send_message(chat_id, text)
        else:
            if h['send_lvlup'] == True:
                bot.send_message(chat_id, text)
    except:
        if h['hunger'] / h['maxhunger'] * 100 <= 30:
            lose_horse(chat_id)


def lose_horse(chat_id):  # returns True on success
    pet = db.chats.find_one({'id': chat_id})
    db.chats.delete_one({'id': chat_id})

    db.lost.insert_one(pet)
    horse_id = db.lost.count_documents({'id': {'$exists': True}})
    while db.lost.find_one({'id': horse_id}) is not None:
        horse_id += 1
    db.lost.update_one({'id': chat_id}, {'$set': {'id': horse_id}})
    db.lost.update_one({'id': horse_id}, {'$set': {'type': 'horse'}})
    return True


def take_horse(horse_id, new_chat_id):
    db.lost.update_one({'id': horse_id}, {'$set': {'id': new_chat_id}})
    pet = db.lost.find_one({'id': new_chat_id})
    db.lost.delete_one({'id': new_chat_id})
    db.chats.insert_one(pet)


def check_new_season():
    x = db.curses.find_one({})
    z = x['season']
    if time.time() - x['lastseason'] >= 2678400:
        new_season(z)
        z += 1
        db.curses.update_one({}, {'$set': {'lastseason': time.time(), 'season': z}})


def check_newday():
    t = threading.Timer(60, check_newday)
    t.start()
    try:
        pass
        #check_new_season()
    except:
        bot.send_message(admin_id, traceback.format_exc())
    x = time.ctime()
    x = x.split(" ")
    ind = 0
    num = 0
    for ids in x:
        for idss in ids:
            if idss == ':':
                tru = ids
                ind = num
        num += 1
    x = tru
    x = x.split(":")
    y = int(x[1])  # минуты
    x = int(x[0]) + 3  # часы (+3, потому что heroku в Великобритании)
    z = time.ctime()

    if y == 0 and x == 24:
        choose_elites()




def is_from_admin(m):
    return m.from_user.id == admin_id

threading.Thread(target=check_all_pets_hunger).start()
threading.Thread(target=check_all_pets_hp).start()
threading.Thread(target=check_newday).start()
threading.Timer(900, check_all_pets_lvlup).start()

bot.send_message(admin_id, 'Бот встал.')

bot.polling()