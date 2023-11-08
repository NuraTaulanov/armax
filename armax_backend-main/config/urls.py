
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request/', include("request.urls")),
    path('webhook/', include('botapp.urls')),
    # path('whatsapp_bot/',include('whatsapp_bot.urls'))
]
