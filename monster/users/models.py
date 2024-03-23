from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from django.contrib import admin
    
class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    objects = UserManager() 
    
    class Meta:
        verbose_name_plural = 'Пользователь'
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.email}'


class UserAdmin(admin.ModelAdmin):
    search_fields = ("email",)

