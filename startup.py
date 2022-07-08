import random
import traceback
from constants import *
from config import *
from lambdas import *
from db import Database
from telebot import types, TeleBot
import threading
import time


bot = TeleBot(token)
db = Database(mongo_url)