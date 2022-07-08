from startup import *

def is_actual(m):
    return m.date + 120 > int(round(time.time()))

def pet_abils_enabled(m):
    return pet_abils

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
    if user.type != 'creator':
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
    if admin_lambda(m):
        return True

    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.type not in {'creator', 'administrator'}:
        bot.respond_to(m, 'Только админ может делать это!') if not silent else None
        return False
    return True