from django.contrib import admin
from .models import User, Chat

class UserAdmin(admin.ModelAdmin):
    pass

class ChatAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Chat, ChatAdmin)