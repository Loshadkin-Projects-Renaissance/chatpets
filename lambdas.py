from startup import *

def is_actual(m):
    return m.date + 120 > int(round(time.time()))

def block_lambda(m):
    return m.chat.id in block or m.from_user.id in block

def register_user(m):
    if db.users.find_one({'_id': m.from_user.id}):
        db.users.update_one({'_id': m.from_user.id}, {'$set': {'time': time.time()}})
    else:
        db.create_user(m.from_user)

def pet_abils_enabled(m):
    return pet_abils

def name_lambda(m):
    if m.chat.id in totalban or m.from_user.id in totalban:
        bot.send_message(m.chat.id,
                                'Вам было запрещено менять имя питомца! Разбан через рандомное время (1 минута - 24 часа).')
        return
    if not horse_admin_lambda(m):
        return
    if not arguments_lambda(m):
        bot.send_message(m.chat.id,
                             'Для переименования используйте формат:\n/name *имя*\nГде *имя* - имя вашего питомца.',
                             parse_mode='markdown')
        return
    if not (2 <= len(m.text) <= 50):
        bot.send_message(m.chat.id, 'Имя должно быть от 2 до 50 символов.')
        return
    return True
    
def throwh_lambda(c):
    if not c.data.startswith('throwh'):
        return
    if c.message.chat.id in ban:
        medit('Можно выгонять только одного питомца в час!', c.message.chat.id, c.message.message_id)
        return
    if db.chats.find_one({'id': c.message.chat.id}) is None:
        medit("У вас даже лошади нет, а вы ее выкидывать собрались!", c.message.chat.id, c.message.message_id)
        return
    user = bot.get_chat_member(c.message.chat.id, c.from_user.id)
    chat = db.chat_admins.find_one({'id': c.message.chat.id})
    if c.message.chat.type == 'private':
        return True
    if chat:
        if m.from_user.id in chat['admins']:
            return True
    if user.status in {'creator', 'administrator'}:
        return True
    return False


def cock_ability(m):
    if not pet_abils_enabled(m):
        return
    if not horse_admin_lambda(m):
        return
    if not reply_lambda(m):
        bot.send_message(m.chat.id, 'Сделайте реплай на сообщение юзера!')
        return

    chat = db.chats.find_one({'id': m.chat.id})
    if not chat:
        return
    if chat['type'] != 'cock':
        bot.send_message(m.chat.id, 'Только петух может делать это!')
        return
    if time.time() - chat['cock_check'] < 1800:
        bot.send_message(m.chat.id, 'Ещё не прошло пол часа с момента предыдущей проверки!')
        return
    return True
    

def admin_lambda(m):
    return m.from_user.id == admin_id

def creator_lambda(m, silent=False):
    if admin_lambda(m):
        return True

    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status != 'creator':
        bot.respond_to(m, 'Только создатель чата может делать это!') if not silent else None
        return False
    return True

def arguments_lambda(m):
    if not m.text.count(' '):
        bot.reply_to(m, f'Неверный формат. Попробуйте {m.text} <аргументы>.')
        return
    return True

def reply_lambda(m, silent=True):
    if not m.reply_to_message:
        bot.send_message(m.chat.id, 'Сделайте реплай на сообщение цели!') if not silent else None
        return
    return True

def horse_admin_lambda(m):
    if chat_admin_lambda(m, True):
        return True

    chat = db.chat_admins.find_one({'id': m.chat.id})
    if not chat:
        return False
    if m.from_user.id not in chat['admins']:
        bot.send_message(m.chat.id, 'Только админ питомца может делать это! Выставить админов может создатель чата по команде: /set_admin. Убрать админа можно командой /remove_admin.')
        return False
    return True

def chat_admin_lambda(m, silent=False):
    if m.chat.type == 'private':
        return True
    if admin_lambda(m):
        return True

    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status not in {'creator', 'administrator'}:
        bot.respond_to(m, 'Только админ может делать это!') if not silent else None
        return False
    return True