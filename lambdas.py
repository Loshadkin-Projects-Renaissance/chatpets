from config import *
from constants import *

def admin_lambda(m):
    return m.from_user.id == admin_id

def arguments_lambda(m):
    return m.text.count(' ')

def reply_lambda(m):
    return m.reply_to_message