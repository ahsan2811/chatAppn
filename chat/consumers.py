from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, UserChannel
from accounts.models import Account
import datetime
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        try:
            user_channel = UserChannel.objects.get(user=self.scope.get('user'))
            user_channel.channel_name=self.channel_name
            user_channel.save()
        except:
            user_channel=UserChannel.objects.create(user=self.scope.get('user'),
                                                    channel_name=self.channel_name)
            user_channel.save()
        self.person_id=self.scope.get("url_route").get("kwargs").get("id")
        
    
    def receive(self, text_data):
        data=json.loads(text_data)
        receiver=Account.objects.get(id=self.person_id)
        message=data.get("message")
        
        if data.get('type')=="new_message":
            now=datetime.datetime.now()
            date=now.date()
            time=now.time()
            new_message=Message.objects.create(sender=self.scope.get('user'),
                                               receiver=receiver,
                                               message=message,
                                               seen=False,
                                               date=date,
                                               time=time)
            new_message.save()
            try:
                data_send={"type":"receiver_function",
                           "type_of_data":"new_message",
                           "data":message}
                user_channel=UserChannel.objects.get(user_id=self.person_id)
                async_to_sync(self.channel_layer.send)(user_channel.channel_name, data_send)
            except:
                pass

        elif data.get("type")=="message_seen":
            user_channel=UserChannel.objects.get(user_id=self.person_id)
            messages=Message.objects.filter(sender=receiver, receiver=self.scope.get('user'))
            messages.update(seen=True)
            data={"type":"receiver_function",
                  "type_of_data":"message_seen"}
            async_to_sync(self.channel_layer.send)(user_channel.channel_name, data)
        elif data.get("type")=="entered_chat":
            try:
                user_channel=UserChannel.objects.get(user_id=self.person_id)
                messages=Message.objects.filter(sender=receiver, receiver=self.scope.get('user'))
                messages.update(seen=True)
                data={"type":"receiver_function",
                    "type_of_data":"message_seen"}
                async_to_sync(self.channel_layer.send)(user_channel.channel_name, data)
            except:
                pass
    def receiver_function(self, data):
        data_to_send=json.dumps(data)
        self.send(data_to_send)
        
        