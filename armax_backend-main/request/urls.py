from django.urls import path
from .views import CreateRequestView, CreateTGBotRequestView

urlpatterns = [
    path('create/', CreateRequestView.as_view()),
    path('create/tgbot', CreateTGBotRequestView.as_view())
]
