from django.db import models
from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from request.models import Request,NICHE_CHOICES
from config.settings import TELEGRAM_BOT_TOKEN,WEBHOOK_URL

TOKEN = TELEGRAM_BOT_TOKEN

bot = TeleBot(TOKEN, threaded=False)

class UpdateBot(APIView):
    def post(self, request):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({'code': 200})

user_responses = {}

questions_submit = [
    "Введите Ваше имя:",
    "Введите Ваш номер телефона:",
    "Введите Вашу почту:",
    "Опишите кратко свой проект:",
    "Введите примерные сроки проекта:",
    "Введите бюджет на проект:"
]

def ask_next_question(chat_id):
    if chat_id in user_responses:
        if user_responses[chat_id]["current_question"] < len(questions_submit):
            question = questions_submit[user_responses[chat_id]["current_question"]]
            bot.send_message(chat_id, question)
        else:

            bot.send_message(chat_id, f'Спасибо за ответы! Мы свяжемся с вами!')

            save_user_responses(chat_id, user_responses[chat_id].get("Ниша"))

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # Отправляем видео и описание
    bot.send_video(chat_id, video=open('/Users/a1/Desktop/armax_backend-main/Untitled video (2).mp4', 'rb'))
    bot.send_message(chat_id, 'Вас приветствует бот компании Armax. Мы компания, которая занимается разработкой всех важнейших решений в области инновации и автоматизации бизнес-процессов. Для перехода с меню введите /. Наши услуги предоавлены кнопке. ')

    # Создаем клавиатуру с кнопкой "Начать"
    start_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Начать', callback_data='start')]])
    bot.send_message(chat_id, 'Нажмите "Начать", чтобы продолжить', reply_markup=start_keyboard)

# Орабтка команды /faq
@bot.message_handler(commands=['faq'])
def faq_message(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,'Какие гарантии на выполнение заказа в соответствии с договором?\nГарантом выступает квазигосударственная организация')

@bot.message_handler(commands=['contacts'])
def faq_message(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,'Project manager\nШакиров Баглан\nshakirovBaglan@gmail.com\n+7 777 777 77 77')

@bot.message_handler(commands=['restart'])
def faq_message(message):
    start_message(message)


@bot.message_handler(commands=['feedback'])
def faq_message(message):
    start_message(message)

# Обработка нажатия кнопки "Начать"
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def handle_start_callback(query):
    chat_id = query.message.chat.id

    # Создаем клавиатуру с другими кнопками (NICHE_CHOICES)
    niche_keyboard = InlineKeyboardMarkup()
    for choice in NICHE_CHOICES:
        button = InlineKeyboardButton(choice[1], callback_data=str(choice[0]))
        niche_keyboard.add(button)
    # Отправляем сообщение с новой клавиатурой
    bot.edit_message_text(text='Выберите платформу', chat_id=chat_id, message_id=query.message.message_id, reply_markup=niche_keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    niche_id = int(call.data)
    niche_text = "Не указано"
    for choice_id, choice_text in NICHE_CHOICES:
        if choice_id == niche_id:
            niche_text = choice_text
            break
    bot.send_message(call.message.chat.id, f'Вы выбрали платформу: {niche_text}')

    chat_id = call.message.chat.id
    if chat_id not in user_responses:
        user_responses[chat_id] = {}
    user_responses[chat_id]["Ниша"] = niche_id 
    user_responses[chat_id]["current_question"] = 0
    ask_next_question(chat_id)

@bot.message_handler(func=lambda message: message.chat.id in user_responses)
def handle_user_responses(message):
    chat_id = message.chat.id
    if chat_id not in user_responses:
        return

    current_question = questions_submit[user_responses[chat_id]["current_question"]]
    user_responses[chat_id][current_question] = message.text

    user_responses[chat_id]["current_question"] += 1
    ask_next_question(chat_id)

def save_user_responses(chat_id, niche):
    if chat_id in user_responses:
        responses = user_responses[chat_id]
        Request.objects.create(
            full_name=responses.get("Введите Ваше имя:"),
            phone=responses.get("Введите Ваш номер телефона:"),
            email=responses.get("Введите Вашу почту:"),
            niche=niche,
            project_desc=responses.get("Опишите кратко свой проект:"),
            project_deadlines=responses.get("Введите примерные сроки проекта:"),
            project_budget=responses.get("Введите бюджет на проект:")
        )
        del user_responses[chat_id]

def save_user_feedback(chat_id,feedback):
    if chat_id in user_responses:
        responses = user_responses[chat_id]
        Feedback.objects.create(
            full_name=responses.get("Введите Ваше имя:"),
            
            email=responses.get("Введите Вашу почту:"),
            
            project_desc=responses.get("Опишите кратко свой проект:"),
            project_deadlines=responses.get("Введите примерные сроки проекта:"),
            project_budget=responses.get("Введите бюджет на проект:")
        )
        del user_responses[chat_id]

# Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
