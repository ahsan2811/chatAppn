from django.db import models
from accounts.models import Account
import datetime
# Create your models here.
class Message(models.Model):
    message=models.TextField()
    sender=models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    receiver=models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='message_receiver')
    seen=models.BooleanField(default=False)
    date=models.DateField(null=True)
    time=models.TimeField(null=True)
    

    
    def __str__(self):
        return self.message

class Friend(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    friend=models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_user')
    
    def __str__(self):
        return f"{self.user.first_name} friend => {self.friend.first_name}"

class FriendRequest(models.Model):
    sender=models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver=models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="request_receiver")
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.first_name} {self.status}"
    

class UserChannel(models.Model):
    channel_name=models.CharField(max_length=50)
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.channel_name