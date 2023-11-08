import os
from django.conf import settings
from config.settings import TELEGRAM_BOT_TOKEN, WEBHOOK_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from telebot import TeleBot, types
from django.db import models
from request.models import Request
from request.models import NICHE_CHOICES
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from time import sleep

TOKEN = TELEGRAM_BOT_TOKEN

bot = TeleBot(TOKEN, threaded=False)


class UpdateBot(APIView):
    def post(self, request):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({'code': 200})



questions = [
    "Введите Ваше имя:",
    "Введите Ваш номер телефона:",
    "Введите Вашу почту:",
    "Опишите кратко свой проект:",
    "Введите примерные сроки проекта:",
    "Введите бюджет на проект:"
]

# Создаем Unicode символы для флагов
kazakhstan_flag_emoji = '🇰🇿'
russian_flag_emoji = '🇷🇺'
greatbritain_flag_emoji = '🇬🇧'

chat_language = {}

class LanguageHandler:
    def __init__(self,language,chat_id):
        self.language=language
        self.chat_id=chat_id
        chat_language[chat_id]=language

    def start(self):
        self.send_video()
        self.send_start_message()

    def send_start_message(self):
        bot.send_message(self.chat_id,self.start_language_text(),reply_markup=self.get_keyboard())
    
    def send_video(self):
        bot.send_video(self.chat_id,self.get_video())

    def start_language_text(self):
        if self.language=='казакша':
            return 'Сәлеметсіз бе, Мен сіздің жеке көмекшіңіз Armax ботымын'
        elif self.language=='русский':
            return 'Здравствуйте, я ваш личный помощник бот Armax'
        elif self.language=='английский':
            return 'Hello, I am your personal assistant bot Armax'

        
    def choose_question_language(self):
        if self.language=='казакша':
            return 'Сізді үнататын сұраулардан таңдаңыз.'
        elif self.language=='русский':
            return 'Выберите интересующий вас вопрос:'
        elif self.language=='английский':
            return "Choose the question you're interested in:"
    
    def get_kazakh_keyboard(self):
        kazakh_keyboard=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        kazakh_buttons = [
            KeyboardButton('Қажетті сұраулар'),
            KeyboardButton('Кері байланыс'),
            KeyboardButton('Байланыс'),
            KeyboardButton('Тілді ауыстыру'),
            KeyboardButton('Ботты қайта іске қосу'),
        ]
        kazakh_keyboard.add(*kazakh_buttons)
        return kazakh_keyboard
    
    def get_russian_keyboard(self):
        russian_keyboard=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        russian_buttons = [
            KeyboardButton('Частые вопросы'),
            KeyboardButton('Обратная связь'),
            KeyboardButton('Контакты'),
            KeyboardButton('Поменять язык'),
            KeyboardButton('Перезапуск бота'),
        ]
        russian_keyboard.add(*russian_buttons)
        return russian_keyboard
    
    def get_english_keyboard(self):
        english_keyboard=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        english_buttons=[
            KeyboardButton('FAQ'),
            KeyboardButton('Feedback'),
            KeyboardButton('Contacts'),
            KeyboardButton('Change language'),
            KeyboardButton('Restart bot'),
        ]
        english_keyboard.add(*english_buttons)
        return english_keyboard
    
    def get_keyboard(self):
        if self.language=='казакша':
            return self.get_kazakh_keyboard()
        elif self.language=='русский':
            return self.get_russian_keyboard()
        elif self.language=='английский':
            return self.get_english_keyboard()

    def get_video(self):
        if self.language=='казакша':
            # video_path = 'video.mp4'
            video_path = 'botapp/static/botapp/video/video.mp4'

            video = open(video_path, 'rb')
            return video
        elif self.language=='русский':
            video_path = 'botapp/static/botapp/video/video.mp4'
            # video_path = 'video.mp4'
            video = open(video_path, 'rb')
            return video
        elif self.language=='английский':
            video_path = 'botapp/static/botapp/video/video.mp4'
            # video_path = 'video.mp4'
            video = open(video_path, 'rb')
            return video
    
@bot.message_handler(commands=['start'])      
def choose_language(message):
    chat_id = message.chat.id
    keyboard_language = InlineKeyboardMarkup()
    kazakhstan_flag_button = InlineKeyboardButton(
        text=f'🇰🇿 Kазақша', callback_data='казакша')
    russian_flag_button = InlineKeyboardButton(
        text=f'🇷🇺 Русский', callback_data='русский')
    english_flag_button = InlineKeyboardButton(
        text=f'🇬🇧 English', callback_data='английский')
    keyboard_language.add(kazakhstan_flag_button, russian_flag_button, english_flag_button)
    bot.send_message(chat_id, '🇷🇺 Выберите язык:\n🇰🇿 Тілді таңдау:\n🇬🇧 Choose a language:', reply_markup=keyboard_language)

faq_answers = {
    'kaz_faq1': "Как мені сізге хабарласуға болады?",
    'kaz_faq2': "Сіз не тағайындау жасау жұмыстарын орындайсыз?",
    'kaz_faq3': "Бот тілін қалай ауыстыруға болады?",
    'kaz_faq4': "Ботты қайта іске қосу қалай?",
    'kaz_faq5': "Armax Studio не қандай?",
    'rus_faq1': "Вы можете связаться с нами по адресу электронной почты: example@email.com",
    'rus_faq2': "Мы предоставляем широкий спектр услуг, включая веб-разработку, мобильную разработку и консультации по ИТ-проектам.",
    'rus_faq3': "Для изменения языка бота, воспользуйтесь командой /setlang и следуйте инструкциям.",
    'rus_faq4': "Для перезапуска бота, просто перезапустите приложение или перезапустите сервер, на котором он работает.",
    'rus_faq5': "Armax Studio - это компания, специализирующаяся на разработке программного обеспечения и веб-проектах.",
    'eng_faq1': "You can contact us via email at example@email.com",
    'eng_faq2': "We offer a wide range of services, including web development, mobile app development, and IT project consulting.",
    'eng_faq3': "To change the bot's language, use the /setlang command and follow the instructions.",
    'eng_faq4': "To restart the bot, simply restart the application or the server it's running on.",
    'eng_faq5': "Armax Studio is a company specializing in software development and web projects.",
    }    


class ButtonHandler:
    def __init__(self, message_text, chat_id):
        self.message_text = message_text
        self.chat_id = chat_id

    def call_keyboards(self):
        keyboard_faq = InlineKeyboardMarkup(row_width=1)

        if self.message_text == 'Байланыс':
            return "TOO 'ARMAX STUDIO'Біздің мекен-жайы: Астана, Қабанбай батыр көшесі, 11/5\nТелефон: +77719052733\nЭлектронды пошта: armax1studio@gmail.com"
        elif self.message_text == 'Контакты':
            return "TOO 'ARMAX STUDIO'\nНаш адрес: Астана, ул. Кабанбай Батыра, 11/5\nТелефон: +77719052733\nЭлектронная почта: armax1studio@gmail.com"
        elif self.message_text == 'Contacts':
            return "TOO 'ARMAX STUDIO'Our address: Astana, Kabanbai Batyr str., 11/5\nPhone: +77719052733\nEmail: armax1studio@gmail.com"
        
        
        elif self.message_text=='Қажетті сұраулар':
            faq_button1 = InlineKeyboardButton(text='Как мені сізге хабарласуға болады?', callback_data='kaz_faq1')
            faq_button2 = InlineKeyboardButton(text='Сіз не тағайындау жасау жұмыстарын орындайсыз?', callback_data='kaz_faq2')
            faq_button3 = InlineKeyboardButton(text='Бот тілін қалай ауыстыруға болады?', callback_data='kaz_faq3')
            faq_button4 = InlineKeyboardButton(text='Ботты қайта іске қосу қалай?', callback_data='kaz_faq4')
            faq_button5 = InlineKeyboardButton(text='Armax Studio не қандай?', callback_data='kaz_faq5')
            keyboard_faq.add(faq_button1, faq_button2, faq_button3, faq_button4, faq_button5)
            return keyboard_faq


        elif self.message_text=='Частые вопросы':
            faq_button1 = InlineKeyboardButton(text='Как я могу связаться с вами?', callback_data='rus_faq1')
            faq_button2 = InlineKeyboardButton(text='Какие услуги вы предоставляете?', callback_data='rus_faq2')
            faq_button3 = InlineKeyboardButton(text='Как изменить язык бота?', callback_data='rus_faq3')
            faq_button4 = InlineKeyboardButton(text='Как перезапустить бота?', callback_data='rus_faq4')
            faq_button5 = InlineKeyboardButton(text='Что такое Armax Studio?', callback_data='rus_faq5')
            keyboard_faq.add(faq_button1,faq_button2,faq_button3,faq_button4,faq_button5)
            return keyboard_faq
        
        elif self.message_text=='FAQ':
            faq_button1 = InlineKeyboardButton(text='How can I contact you?', callback_data='eng_faq1')
            faq_button2 = InlineKeyboardButton(text='What services do you offer?', callback_data='eng_faq2')
            faq_button3 = InlineKeyboardButton(text='How to change the bot language?', callback_data='eng_faq3')
            faq_button4 = InlineKeyboardButton(text='How to restart the bot?', callback_data='eng_faq4')
            faq_button5 = InlineKeyboardButton(text='What is Armax Studio?', callback_data='eng_faq5')
            keyboard_faq.add(faq_button1, faq_button2, faq_button3, faq_button4, faq_button5)
            return keyboard_faq

        
        elif self.message_text=='Кері байланыс':
            return
        elif self.message_text=='Обратная связь':
            return
        elif self.message_text=='Feedback':
            return
        

    def choose_language(self):
        keyboard_language = InlineKeyboardMarkup()
        kazakhstan_flag_button = InlineKeyboardButton(
            text=f'🇰🇿 Kазақша', callback_data='казакша')
        russian_flag_button = InlineKeyboardButton(
            text=f'🇷🇺 Русский', callback_data='русский')
        english_flag_button = InlineKeyboardButton(
            text=f'🇬🇧 English', callback_data='английский')
        keyboard_language.add(kazakhstan_flag_button, russian_flag_button, english_flag_button)
        bot.send_message(self.chat_id, '🇷🇺 Выберите язык:\n🇰🇿 Тілді таңдау:\n🇬🇧 Choose a language:', reply_markup=keyboard_language)

    

# Обработчик для всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    chat_id = message.chat.id
    message_text = message.text
    button_handler = ButtonHandler(message_text, chat_id)
    if message_text == 'FAQ' or message_text == 'Частые вопросы' or message_text=='Қажетті сұраулар':
        # Отобразить Inline-кнопки для часто задаваемых вопросов

        keyboard_faq = button_handler.call_keyboards()
        bot.send_message(chat_id,message_text, reply_markup=keyboard_faq)
    elif message_text == 'Поменять язык' or message_text == 'Change language' or message_text=='Тілді ауыстыру':
        button_handler.choose_language()
    elif message_text == 'Ботты қайта іске қосу' or message_text == 'Перезапуск бота' or message_text=='Restart bot':
        button_handler.choose_language()
    else:
        # В остальных случаях отправить текст или другую информацию
        response_text = button_handler.call_keyboards()
        bot.send_message(chat_id, response_text)

@bot.callback_query_handler(func=lambda call: call.data in ['казакша', 'русский', 'английский'])
def call_choose_language(call):
    chat_id = call.message.chat.id
    language=call.data
    language_handler = LanguageHandler(language,chat_id)
    language_handler.start()

@bot.callback_query_handler(func=lambda call:call.data in faq_answers)
def handle_button(call):
    call_data=call.data
    chat_id=call.message.chat.id
    if call_data in faq_answers:
        bot.send_message(chat_id,faq_answers[call_data])


# Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL+'/webhook/')