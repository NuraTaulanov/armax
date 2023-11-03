from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from request.models import Request, NICHE_CHOICES

questions = {} 

@csrf_exempt
def bot(request):
    sender_number = request.POST.get("From", "")
    user_response = request.POST.get("Body", "").strip().lower()

    if sender_number not in questions:
        questions[sender_number] = {
            "state": 'greet',
            "Введите Ваше имя": "",
            "Введите Ваш номер телефона": "",
            "Введите Вашу почту": "",
            "Опишите кратко свой проект": "",
            "Введите примерные сроки проекта": "",
            "Введите бюджет на проект": ""
        }

    state = questions[sender_number]["state"]
    response = MessagingResponse()

    if state == "greet":
        response.message("Добро пожаловать в наш бот выбора платформы разработки. Введите Ваше имя:")
        questions[sender_number]["state"] = "get_name"
    elif state == "get_name":
        questions[sender_number]["name"] = user_response
        response.message("Введите Ваш номер телефона:")
        questions[sender_number]["state"] = "get_tel"
    elif state == "get_tel":
        questions[sender_number]["tel"] = user_response
        response.message("Введите Вашу почту:")
        questions[sender_number]["state"] = "get_email"
    elif state == "get_email":
        questions[sender_number]["email"] = user_response
        response.message(f'Выберите платформу:\n' + "\n".join([f'{key}) {value[1]}' for key, value in enumerate(NICHE_CHOICES, start=1)]))
        questions[sender_number]["state"] = "get_platform"
    elif state == "get_platform":
        try:
            user_response = int(user_response)  # Преобразуем ответ пользователя в целое число
            if 1 <= user_response <= 4:
                # Получаем числовое значение из NICHE_CHOICES
                questions[sender_number]["platform"] = user_response
                response.message("Вы выбрали {}.".format(NICHE_CHOICES[user_response - 1][1]))
                response.message("Опишите кратко свой проект:")
                questions[sender_number]["state"] = "get_summary"
            else:
                response.message("Пожалуйста, выберите подходящую платформу (1-4).")
        except ValueError:
            response.message("Пожалуйста, введите число от 1 до 4 для выбора платформы.")

    elif state == "get_summary":
        questions[sender_number]["project_summary"] = user_response
        response.message("Введите примерные сроки проекта:")
        questions[sender_number]["state"] = "project_time"
    elif state == "project_time":
        questions[sender_number]["project_time"] = user_response
        response.message("Введите бюджет на проект:")
        questions[sender_number]["state"] = "get_budget"
    elif state == "get_budget":
        questions[sender_number]["budget"] = user_response
        response.message("Благодарим вас за использование нашего бота для выбора платформы.")
        questions[sender_number]["state"] = "complete"

        # Создание и сохранение экземпляра модели Request в базе данных
        request_instance = Request(
            full_name=questions[sender_number]["name"],
            phone=questions[sender_number]["tel"],
            email=questions[sender_number]["email"],
            niche=questions[sender_number]["platform"],
            project_desc=questions[sender_number]["project_summary"],
            project_deadlines=questions[sender_number]["project_time"],
            project_budget=questions[sender_number]["budget"]
        )
        request_instance.save()

        # Сброс состояния пользователя после сохранения ответов
        questions[sender_number] = {}
    else:
        response.message("Благодарим вас за использование нашего бота для выбора платформы.")

    return HttpResponse(str(response))
