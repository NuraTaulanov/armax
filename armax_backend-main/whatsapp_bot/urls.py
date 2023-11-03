from django.urls import path
from .views import bot

urlpatterns = [
    # path('', views.bot, name='bot'),
    path('', bot, name='bot'),

]