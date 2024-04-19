from django.contrib import admin
from .models import UserChannel, Message, FriendRequest, Friend
# Register your models here.
admin.site.register(Message)
admin.site.register(UserChannel)
admin.site.register(Friend)
admin.site.register(FriendRequest)