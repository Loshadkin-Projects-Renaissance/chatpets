# -*- coding: utf-8 -*-
from startup import *
from lambdas import *

@bot.message_handler(func=lambda m: not is_actual(m))
def skip_message(m):
    pass

@bot.message_handler(func=block_lambda)
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
    db.choose_elites()
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

@bot.message_handler(commands=['addkaza'], func=admin_lambda)
def addgoose(m):
    try:
        db.globalchats.update_one({'id': m.chat.id}, {'$push': {'avalaible_pets': 'kaza'}})
        bot.send_message(m.chat.id, 'Ура, коза')
    except:
        pass


@bot.message_handler(commands=['feed'])
def feed_handler(m):
    pet = db.chats.find_one({'id': m.chat.id})
    x = pet
    if pet is None:
        bot.send_message(m.chat.id, 'А кормить некого:(')
        return
    petname = 'missingno'
    spisok = ['missingno']
    s2 = ['missingno']
    spisok, s2, petname = get_feed_text(pet)

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

@bot.message_handler(commands=['feedback'], func=lambda m: reply_lambda(m) or arguments_lambda(m))
def feedback_handler(m):
    message = m
    if m.reply_to_message:
        text = m.reply_to_message.text
        message = m.reply_to_message
    else:
        text = m.text.split(' ', 1)[1]
    tts = f'<b>Сообщение от пользователя</b> {bot.form_html_userlink(m.from_user.first_name, m.from_user.id)}:\n'
    tts += f'\n{text}'
    bot.respond_to(m, 'Сообщение отправлено автору.')
    bot.send_message(admin_id, tts, parse_mode='HTML')
    bot.forward_message(admin_id, m.chat.id, message.message_id)

@bot.message_handler(commands=['scan_chats'], func=admin_lambda)
def scan_chats_handler(m):
    try:
        scan_ch()
    except:
        print(traceback.format_exc())

def scan_ch():
    bot.send_message(admin_id, 'Сканирование начато.')
    print('Подготовка...')
    #db.globalchats.update_many({}, {'$set': {'still': False}})
    print('Фаза первая. Скачивание базы данных.')
    print('Измерение БД...')
    print(f'Размер БД: {db.globalchats.count_documents({})}')
    print('Скачивание БД...')
    all_chats = list(db.globalchats.find({}))
    print(f'БД скачана. Размер: {len(all_chats)}')
    print(f'Фаза вторая: сканирование.')

    for i in range(len(all_chats)):
        chat = all_chats[i]
        print(f'{i}/{len(all_chats)-1}: ПРОВЕРКА НАЛИЧИЯ БОТА В ЧАТЕ.')
        try:
            bot.send_chat_action(chat['id'], 'typing')
            print(f'{i}/{len(all_chats)-1}: УСПЕХ.')
            db.globalchats.update_one({'id': chat['id']}, {'$set': {'still': True}})
        except:
            print(f'{i}/{len(all_chats)-1}: ПРОВАЛ.')
            db.globalchats.update_one({'id': chat['id']}, {'$set': {'still': False}})
    bot.send_message(admin_id, 'Сканирование завершено.')
        

@bot.message_handler(commands=['getpets'], func=admin_lambda)
def getpet(m):
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
def rules_handler(m):
    text = '1. Не использовать клиентских ботов для кормления питомца! За это будут наказания.\n' \
           '2. Не давать рекламу в списке выброшенных питомцев.'
 
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['remove'], func=admin_lambda)
def remove_handler(m):
    try:
        db.lost.delete_one({'id': int(m.text.split(' ')[1])})
        bot.send_message(m.chat.id, "Питомец удален с улицы. НАВСЕГДА.")
    except:
        pass


@bot.message_handler(commands=['start'], func=lambda message: is_actual(message))
def start_handler(m):
    if m.from_user.id != m.chat.id:
        return
    bot.send_message(m.chat.id, 'Здравствуй! /help для информации.')


@bot.message_handler(commands=['info'], func=admin_lambda)
def info_handler(m):
    text = ''

    for ids in db.chats.find({}):
        text += str(ids) + '\n\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['top'], func=lambda message: is_actual(message))
def top_handler(m):
    db_pets = db.chats.find().sort('lvl', -1).limit(10)
    text = 'Топ-10 питомцев:\n\n'

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


@bot.message_handler(commands=['bot_stat'], func=admin_lambda)
def bot_stat_handler(m):
    a = db.chats.count_documents({})
    b = db.globalchats.count_documents({'still': True})
    c = db.globalchats.count_documents({})
    c1 = db.globalchats.count_documents({'active': True})
    d1 = db.users.count_documents({})
    d2 = db.users.count_documents({'now_elite': True})
    d3 = db.users.count_documents({'active': True})
    e = db.curses.find_one({})
    e1 = e['season']
    e2 = date.fromtimestamp(e['lastseason']).strftime('%H:%M:%S %d.%m.%y')
    tts = f'📊Статистика бота:\n'
    tts += f'💬Чаты: {a}|{c1}|{b}|{c}\n'
    tts += f'👤Пользователи: {d3}|{d2}|{d1}\n'
    tts += f'🍂Сезон: {e1}|{e2}'
    bot.respond_to(m, tts)


@bot.message_handler(commands=['help'])
def help(m):
    text = ''
    text += 'Чатовые питомцы питаются активностью юзеров. Чем больше вы общаетесь в чате, тем счастливее будет питомец! '
    text += 'Если долго не общаться, питомец начинает голодать и терять жизни. Назвать питомца можно командой /name\n'
    text += 'Для получения опыта необходимо иметь 85% сытости. Для получения бонусного опыта - 90% и 99% (за каждую отметку дается x опыта. То есть если у вас 90% сытости, вы получите (базовый_опыт + х), а если 99%, то (базовый_опыт + 2х).'

    bot.send_message(m.chat.id, text)


@bot.message_handler(func=lambda message: message.migrate_from_chat_id is not None, content_types=None)
def migrate_handler(m):
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
def achlist_handler(m):
    text = '1. За каждые 100 уровней даётся по 1 кубику, и так до 10000го.\n'
    text += '2. За актив в чате (сообщения от 10ти пользователей за минуту) даётся 3 кубика!\n'
    text += 'В будущем я добавлю секретные ачивки (но вам об этом не скажу)! Список ачивок будет пополняться.'

    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['addexp'], func=admin_lambda)
def addexp(m):
    try:
        db.chats.update_one({'id': m.chat.id}, {'$inc': {'exp': int(m.text.split(' ')[1])}})
    except:
        pass


@bot.message_handler(commands=['addhunger'], func=admin_lambda)
def addexp(m):
    try:
        db.chats.update_one({'id': m.chat.id},
                            {'$inc': {'maxhunger': int(m.text.split(' ')[1]), 'hunger': int(m.text.split(' ')[1])}})
    except:
        pass


@bot.message_handler(commands=['addlvl'], func=admin_lambda)
def addlvl(m):
    try:
        db.chats.update_one({'id': m.chat.id}, {'$inc': {'lvl': int(m.text.split(' ')[1])}})
    except:
        pass


@bot.message_handler(commands=['reboot'], func=admin_lambda)
def addlvl(m):
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
    text = emoj + 'Имя: ' + animal['name'] + '\n'
    text += '🏅Уровень: ' + str(animal['lvl']) + '\n'
    text += '🔥Опыт: ' + str(animal['exp']) + '/' + str(nextlvl(animal)) + '\n'
    text += '♥Здоровье: ' + str(animal['hp']) + '/' + str(animal['maxhp']) + '\n'
    p = int(animal['hunger'] / animal['maxhunger'] * 100)
    text += '🍔Сытость: ' + str(animal['hunger']) + '/' + str(animal['maxhunger']) + ' (' + str(p) + '%)' + '\n'
    text += 'Нужно сытости для постоянного получения опыта: ' + str(int(animal['maxhunger'] * 0.85))

    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['losthorses'], func=lambda message: is_actual(message))
def losthorses(m):
    if db.lost.count_documents({'id': {'$exists': True}}) == 0:
        bot.send_message(m.chat.id, "На улице питомцев нет!")
        return
    text = 'Чтобы забрать питомца, введите команду /takeh id\n\n'
    for pet in db.lost.find({'id': {'$exists': True}}):
        text += f'{pettoemoji(pet["type"])}{pet["id"]}: {pet["name"]} ({pet["lvl"]} лвл)\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['takeh'], func=lambda message: is_actual(message))
def takeh(m):
    try:
        horse_id = int(m.text.split(' ')[1])
        if db.lost.find_one({'id': horse_id}) is None:
            bot.send_message(m.chat.id, "Питомец не существует!")
            return
        if db.chats.find_one({'id': m.chat.id}) is not None:
            bot.send_message(m.chat.id, "У вас уже есть питомец!")
            return
        db.take_horse(horse_id, m.chat.id)
        db.chats.update_one({'id': horse_id}, {'$set': {'id': m.chat.id}})
        bot.send_message(m.chat.id,
                             "Поздравляем, вы спасли питомца от голода! Следите за ним, чтобы он рос и не голодал!")
    except:
        pass


def unban(id):
    try:
        ban.remove(id)
    except:
        pass


@bot.message_handler(commands=['throwh'])
def throwh(m):
    if m.chat.id not in ban:
        if db.chats.find_one({'id': m.chat.id}) is None:
            bot.send_message(m.chat.id, "У вас даже лошади нет, а вы ее выкидывать собрались!")
            return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Подтверждаю.', callback_data='throwh ' + str(m.from_user.id)),
               types.InlineKeyboardButton(text='Отмена!', callback_data='cancel ' + str(m.from_user.id)))
        bot.send_message(m.chat.id, 'Подтвердите, что вы хотите выбросить лошадь.', reply_markup=kb)
    else:
        bot.send_message(m.chat.id, 'Выкидывать питомца можно только раз в час!')
        return


@bot.message_handler(commands=['ban'], func=lambda m: admin_lambda(m) and arguments_lambda(m))
def ban_handler(m):
    totalban.append(int(m.text.split(' ')[1]))
    bot.send_message(m.chat.id, 'Бан.')


@bot.message_handler(commands=['name'], func=name_lambda)
def name_handler(m):
    name = m.text.split(' ', 1)[1]

    if db.chats.find_one({'id': m.chat.id}) is None:
        bot.send_message(m.chat.id, 'Для начала питомца нужно завести (/growpet)!')
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



@bot.message_handler(commands=['addcube'], func=admin_lambda)
def addcube_handler(m):
    try:
        db.globalchats.update_one({'id': m.chat.id}, {'$inc': {'pet_access': int(m.text.split()[1])}})
        bot.send_message(m.chat.id, 'Успешно выдано ' + m.text.split()[1] + ' кубов!')
    except:
        bot.send_message(m.chat.id, 'Возможно, вы забыли указать количество. Хотя хз.')


@bot.message_handler(commands=['use_dice'], func=chat_admin_lambda)
def use_dice(m):
    chat = db.globalchats.find_one({'id': m.chat.id})
    if not chat:
        return
    if chat['pet_access'] > 0:
        pet = random.choice(alltypes)
        db.give_pet(m.chat.id, pet)
        bot.send_message(m.chat.id, 'Кручу-верчу, питомца выбрать хочу...\n...\n...\n...\n...\n...\nПоздравляю! Вам достался питомец "*' + pettype(
                                 pet) + '*"!', parse_mode='markdown')
    else:
        bot.send_message(m.chat.id, 'У вас нет кубов! Зарабатывайте достижения для их получения!')

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
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['allinfo'], func=admin_lambda)
def allinfo(m):
    text = str(db.chats.find_one({'id': m.chat.id}))
    bot.send_message(admin_id, text)


@bot.message_handler(commands=['great_igogo'], func=lambda m: arguments_lambda(m) and admin_lambda(m))
def announce(m):
    bot.respond_to(m, f'Начал.')
    text = m.text.split(' ', 1)[1]
    try:
        i = hypercast(text)
    except:
        print(traceback.format_exc())
        i = -1
    bot.send_message(m.chat.id, f"Сообщение успешно получило {i}/{len(chat_ids)} чатиков")

def hypercast(text):
    chats_ids = db.globalchats.find({'still': True})
    i = 0
    for doc in chats_ids:
        print(f'{i}/1900')
        try:
            bot.send_message(doc['id'], text)
            i += 1
        except:
            pass
    return i


@bot.message_handler(commands=['igogo'], func=lambda m: arguments_lambda(m) and admin_lambda(m))
def announce(m):
    text = m.text.split(' ', 1)[1]
    chats_ids = db.chats.find({})
    i = 0
    for doc in chats_ids:
        try:
            bot.send_message(doc['id'], text)
            i += 1
        except:
            pass
    bot.send_message(m.chat.id, f"Сообщение успешно получило {i}/{len(chats_ids)} чатиков")


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
            bot.send_message(m.chat.id, 'Открыто достижение "Так просто?"! Награда: 2 куба.')

            bot.send_message(admin_id,
                             m.from_user.first_name + '(' + str(m.from_user.username) + ') открыл секрет!')
        else:
            bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')

    else:
        bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')


@bot.message_handler(commands=['select_pet'], func=lambda m: arguments_lambda(m) and chat_admin_lambda(m))
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
    if newpet in chat['avalaible_pets']:
        db.chats.update_one({'id': m.chat.id}, {'$set': {'type': newpet}})
        bot.send_message(m.chat.id, 'Вы успешно сменили тип питомца на "' + pet + '"!')
    else:
        bot.send_message(m.chat.id, 'Вам сейчас не доступен этот тип питомцев!')

def new_season(ses):
    bot.send_message(admin_id, 'Начинается новый сезон.')
    for ids in db.chats.find({}):
        x = db.globalchats.find_one({'id': ids['id']})
        if x == None:
            db.globalchats.insert_one(db.form_globalchat(ids['id']))
            x = db.globalchats.find_one({'id': ids['id']})
        db.globalchats.update_one({'id': ids['id']}, {'$set': {'saved_pets.' + str(ids['id']) + 'season' + str(ses): ids}})
        if ids['lvl'] > x['pet_maxlvl']:
            db.globalchats.update_one({'id': ids['id']}, {'$set': {'pet_maxlvl': ids['lvl']}})
    
    db.globalchats.update_many({}, {'$set': {'new_season': True}})
    db_pets = db.chats.find().sort('lvl', -1).limit(10)
    for doc in db_pets:
        db.globalchats.update_one({'id': doc['id']}, {'$inc': {'pet_access': 3}})
    for ids in db.chats.find({}):
        try:
            bot.send_message(ids['id'],
                             'Начинается новый сезон! Все ваши текущие питомцы добавлены вам в дом, но кормить их больше не нужно, и уровень у них больше не поднимется. Они останутся у вас как память. Все чаты из топ-10 получают 3 куба в подарок!')
        except:
            pass
    db.chats.delete_many({})
    db.lost.delete_many({})
    bot.send_message(admin_id, 'Новый сезон начался!')


@bot.message_handler(content_types=['text'])
def messages(m):
    if random.randint(1, 100) <= 80:
        return
    if db.users.find_one({'id': m.from_user.id}) == None:
        db.create_user(m.from_user)
    if m.from_user.first_name == 'Telegram':
        pass
    db.users.update_one({'id': m.from_user.id}, {'$set': {'active': True, 'time': time.time()}})
    if db.globalchats.find_one({'id': m.chat.id}) == None:
        db.globalchats.insert_one(db.form_globalchat(m.chat.id))
    db.globalchats.update_one({'id': m.chat.id}, {'$set': {'active': True, 'time': time.time()}})

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



@bot.callback_query_handler(func=throwh_lambda)
def throwh_call_handler(call):
    c = call
    if db.lose_horse(call.message.chat.id):
        ban.append(call.message.chat.id)
        threading.Timer(3600, unban, args=[call.message.chat.id]).start()
        medit("Вы выбросили питомца на улицу... Если его никто не подберет, он умрет от голода!",
                    call.message.chat.id, call.message.message_id)

    else:
        medit(
            "На улице гуляет слишком много лошадей, поэтому, как только вы ее выкинули, лошадь украли цыгане!",
            call.message.chat.id, call.message.message_id)
        


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel'))
def cancel_call_handler(call):
    if call.from_user.id == int(call.data.split(' ')[1]):
        medit('Отменено.', call.message.chat.id, call.message.message_id)


    

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
        if len(lastminutefeed) >= 10 and '10 users in one minute!' not in gchat['achievements']:
            db.globalchats.update_one({'id': pet['id']}, {'$push': {'achievements': '10 users in one minute!'}})
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

def cleanup():
    bot.send_message(admin_id, f'♻️Очищено пользователей: {db.user_cleanup()}')
    bot.send_message(admin_id, f'♻️Очищено чатов: {db.chat_cleanup()}')
    threading.Timer(24*60*60, cleanup).start()

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
            db.lose_horse(chat_id)

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
    x = time.strftime('%M %H').split()
    m = int(x[0])
    h = int(x[1])

    if m == 0 and h == 0:
        try:
            db.choose_elites()
        except:
            bot.send_message(admin_id, traceback.format_exc())


threading.Thread(target=check_all_pets_hunger).start()
threading.Thread(target=check_all_pets_hp).start()
threading.Thread(target=check_newday).start()
threading.Thread(target=cleanup).start()
threading.Timer(900, check_all_pets_lvlup).start()



bot.send_message(admin_id, 'Бот встал.')

try:
    bot.polling()
except:
    bot.send_message(admin_id, 'DIED')
    bot.send_message(admin_id, traceback.format_exc())
    exit(1)
