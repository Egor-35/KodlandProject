import telebot
from telebot import types
import json
import os

# Токен вашего бота
TOKEN = '7919606920:AAErJgiLL9ASlMBEIa8kfVZ9gP-5ms3FHWY'
# Ваш Telegram ID
ADMIN_TELEGRAM_ID = '1877143530'
# Файлы для хранения данных
USER_IDS_FILE = 'user_ids.json'
USER_INFO_FILE = 'user_info.txt'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# Словарь с описаниями и фотографиями моделей
models_info = {
    'Палочки для еды': {
        'description': '100 руб/шт',
        'photo_url': 'https://images.cults3d.com/xuGV64RVUHPBCcMlNI3swSTcazQ=/516x516/filters:no_upscale():format(webp)/https://fbi.cults3d.com/uploaders/25509731/illustration-file/3f763801-737d-41c6-b55f-2ac50300c647/Screenshot-2022-11-14-022030.jpg'
    },
    'Осминоги': {
        'description': '100 руб/шт',
        'photo_url': 'https://images.cults3d.com/yfhiO_EEKIlcLW31k9GnqPbiK3U=/516x516/filters:no_upscale():format(webp)/https://fbi.cults3d.com/uploaders/14456321/illustration-file/0884f383-c610-4e51-a13f-49f2620758f6/IMG_20190316_111642.jpg'
    },
    'Model_3': {
        'description': 'Description for Model 3',
        'photo_url': 'Photo_url_for_Model_3/'
    }
}

# Функция для загрузки ID пользователей из файла
def load_user_ids():
    if os.path.exists(USER_IDS_FILE):
        with open(USER_IDS_FILE, 'r') as file:
            return json.load(file)
    return []


# Функция для сохранения ID пользователей в файл
def save_user_ids(user_ids):
    with open(USER_IDS_FILE, 'w') as file:
        json.dump(user_ids, file)


# Функция для записи информации о пользователях в файл
def save_user_info(user_id, username):
    with open(USER_INFO_FILE, 'a') as file:
        file.write(f"{user_id} {username}\n")


# Загрузка ID пользователей
user_ids = load_user_ids()


# Обработчик для кнопки "/start"
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Информация')
    itembtn2 = types.KeyboardButton('Купить')
    itembtn3 = types.KeyboardButton('Предложить модель')

    # Проверка имени пользователя
    if message.chat.username == 'egorroi35':
        itembtn4 = types.KeyboardButton('Test')
        markup.add(itembtn4)

    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Привет! Я бот-магазин 3д печати. Чем я могу помочь?", reply_markup=markup)

    # Сохраняем ID и имя пользователя
    if message.chat.id not in user_ids:
        user_ids.append(message.chat.id)
        save_user_ids(user_ids)
        save_user_info(message.chat.id, message.chat.username)

# Обработчик для кнопки "Buy"
@bot.message_handler(func=lambda message: message.text == 'Купить')
def handle_buy(message):
    send_models_keyboard(message.chat.id)

# Обработчик для кнопки "Suggest Model"
@bot.message_handler(func=lambda message: message.text == 'Предложить модель')
def handle_offer_model(message):
    offer_message = ("Предложите модель для каталога, "
                     "зайдите на сайт [thingiverse](https://www.thingiverse.com/) или на [cults3d](https://cults3d.com/) или на другой любой сайт "
                     "и выберите модель, затем отправьте ее боту.")
    bot.send_message(message.chat.id, offer_message, parse_mode='Markdown')

# Обработчик для кнопки "Questions"
@bot.message_handler(func=lambda message: message.text == 'Информация')
def handle_questions(message):
    help_message = (
        "Информация о магазине\n\n"
        "Основные функции бота:\n"
        "Купить: Выбирайте и заказывайте 3D-модели. Бот показывает доступные модели, что позволяет легко оформить заказ.\n"
        "Предложить модель: Если у вас есть идея новой 3D-модели, нажмите эту кнопку и отправьте нам свою идею.\n"
        "Примечание. Если у вас нету ника, то с вами связаться не смогут. Бот не принимает текстовые сообщения. Все действия выполняются нажатием кнопок."
        "Если у вас есть другие вопросы, нажмите «Задать вопрос», и бот предложит вам ввести вопрос. "
        "Ваш вопрос будет добавлен в поддержку бота.\n"
    )

    markup = types.InlineKeyboardMarkup()
    ask_question_button = types.InlineKeyboardButton(text="Задать вопрос", callback_data="ask_question")
    markup.add(ask_question_button)

    bot.send_message(message.chat.id, help_message, reply_markup=markup)

# Обработчик для кнопки "Ask a question"
@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def handle_ask_question(call):
    bot.send_message(call.message.chat.id, "Задайте свой вопрос:")
    bot.register_next_step_handler(call.message, receive_question)

# Обработчик получения вопроса от пользователя
def receive_question(message):
    user_question = message.text
    if user_question:
        bot.send_message(message.chat.id, "Мы добавим этот вопрос в поддержку бота.")
        bot.send_message(ADMIN_TELEGRAM_ID, f"Новый вопрос от пользователя: {user_question}")
    else:
        bot.send_message(message.chat.id, "Вопрос не получен. Пожалуйста, попробуйте еще раз.")

# Функция для отправки клавиатуры с кнопками моделей
def send_models_keyboard(chat_id):
    markup = types.InlineKeyboardMarkup()
    for model_name in models_info:
        button = types.InlineKeyboardButton(text=model_name, callback_data=model_name)
        markup.add(button)
    bot.send_message(chat_id, "Выберите, какую модель вы хотите купить:", reply_markup=markup)

# Обработчик для обработки нажатия на кнопку "Buy Model"
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_model(call):
    model_name = call.data.split('_')[1]
    user_name = call.message.chat.username if call.message.chat.username else "User"
    bot.send_message(ADMIN_TELEGRAM_ID, f"https://t.me/{user_name} хочет купить модель {model_name}.")
    bot.send_message(call.message.chat.id, "Мы свяжемся с вами в ближайшее время для уточнения деталей заказа.")

# Обработчик для кнопки "Back"
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Обработчик для кнопки "Test"
@bot.message_handler(func=lambda message: message.text == 'Test' and message.chat.username == 'egorroi35')
def handle_test(message):
    markup = types.InlineKeyboardMarkup()
    btn_off = types.InlineKeyboardButton(text="Turn off bot", callback_data="turn_off")
    btn_on = types.InlineKeyboardButton(text="Turn on bot", callback_data="turn_on")
    btn_post = types.InlineKeyboardButton(text="Send post", callback_data="send_post")
    markup.add(btn_off, btn_on, btn_post)

    bot.send_message(message.chat.id, 'Test menu', reply_markup=markup)


# Обработчик для других пользователей, если они отправляют "Test"
@bot.message_handler(func=lambda message: message.text == 'Test' and message.chat.username != 'egorroi35')
def handle_test_other_users(message):
    bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")


# Обработчики для инлайн-кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'turn_off')
def handle_turn_off(call):
    bot.send_message(call.message.chat.id, "Bot is turned off.")

@bot.callback_query_handler(func=lambda call: call.data == 'turn_on')
def handle_turn_on(call):
    bot.send_message(call.message.chat.id, "Bot is turned on.")

@bot.callback_query_handler(func=lambda call: call.data == 'send_post')
def handle_send_post_init(call):
    bot.send_message(call.message.chat.id, "Напишите содержание поста для всех пользователей:")
    bot.register_next_step_handler(call.message, get_post_content)


# Обработчик для получения текста поста
def get_post_content(message):
    post_message = message.text
    if post_message:
        bot.send_message(message.chat.id, "Сообщение было разослано всем пользователям.")
        send_post_to_all_users(post_message)
    else:
        bot.send_message(message.chat.id, "Сообщение не может быть пустым.")


# Функция для отправки поста всем пользователям
def send_post_to_all_users(post_message):
    for user_id in user_ids:
        try:
            bot.send_message(user_id, post_message)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

# Обработчик для обработки нажатия на кнопки моделей
@bot.callback_query_handler(func=lambda call: True)
def handle_model_button(call):
    model_name = call.data
    model_info = models_info.get(model_name)
    if model_info:
        description = model_info['description']
        photo_url = model_info['photo_url']
        msg = f"{description}\n\nЧтобы купить данную модель, нажмите кнопку «Купить модель»."
        markup = types.InlineKeyboardMarkup()
        buy_button = types.InlineKeyboardButton(text="Купить модель", callback_data=f"buy_{model_name}")
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="back")
        markup.add(buy_button)
        markup.add(back_button)
        bot.send_photo(call.message.chat.id, photo_url, caption=msg, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "К сожалению, данной модели нет в наличии.")

# Запуск бота
while True:
    bot.polling()
