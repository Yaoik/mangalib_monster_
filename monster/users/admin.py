from django.contrib import admin
from users.models import User, UserAdmin

admin.site.register(User, UserAdmin)