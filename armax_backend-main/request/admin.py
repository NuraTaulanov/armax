from django.contrib import admin
from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id','full_name', 'niche', 'project_deadlines', 'project_budget')
    list_filter = ('niche',)  # Добавляем фильтр по полю 'niche'
    ordering = ('project_deadlines', 'project_budget')  # Сортировка по срокам и бюджету
