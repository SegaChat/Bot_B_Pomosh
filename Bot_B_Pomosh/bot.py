import telebot
import json
from telebot.types import ReplyKeyboardMarkup
from config import my_TOKEN
import logging
from gpt import GPT
from config import MAX_TOKENS

bot = telebot.TeleBot(token=my_TOKEN)
gpt = GPT()

def save_to_json():
    with open('users_history.json', 'w', encoding='utf-8') as f:
        json.dump(users_history, f, indent=2, ensure_ascii=False)

def load_from_json():
    try:
        with open('users_history.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    return data

users_history = load_from_json()

def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w")

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! /n"
                          "Я бот-помощник для решения математических задач\n"
                          f"Ты можешь прислать задачу, а я постараюсь ее решить.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.\n"
                          "Напиши /help для дополнительной информации",
                     reply_markup=create_keyboard(['/help']))

@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="/start - приветствие\n"
                          "/help - помощь\n"
                          "/solve_task - команда, чтобы приступить к запросу к нейросети\n\n"
                          "PS: к сожалению, бот не идеален, он также не застрохован от ошибок",
                     reply_markup=create_keyboard(["/solve_task"]))

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if text in ["пока", "как дела?", "привет"]:
        pass
    elif text == "/solve_task":
        pass
    else:
        pass

@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
    logging.info("Кто-то использовал секретную функцию дебаг...")

if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling()
