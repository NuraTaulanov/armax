from django.db import models

NICHE_CHOICES = (
    (1, "Веб"),
    (2, "Мобильное приложение"),
    (3, "Десктопное приложение"),
    (4, "Кроссплатформенное приложение")
)

class Request(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="Электронная почта")
    niche = models.SmallIntegerField(choices=NICHE_CHOICES, default=0, verbose_name="Ниша")
    project_desc = models.TextField(null=True, blank=True)
    project_deadlines = models.TextField(null=True, blank=True)
    project_budget = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}, {self.get_niche_display()}, {self.project_deadlines}, {self.project_budget}"

class Feedback(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Полное имя")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="Электронная почта")
    feedback=models.CharField(max_length=10000,null=True,blank=True,verbose_name="Обратная связь")
    project_desc = models.TextField(null=True, blank=True)
    