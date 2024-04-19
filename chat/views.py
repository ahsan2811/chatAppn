from django.shortcuts import render, redirect
from accounts.models import Account, UserProfile
from .models import Message, Friend, FriendRequest
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Case, When, BooleanField, Subquery, OuterRef

# Create your views here.
@login_required(login_url='login')
def index(request):
    friends=Friend.objects.filter(user=request.user)
    friends_ids=Friend.objects.filter(user=request.user).values_list('friend', flat=True)
    user_profiles=UserProfile.objects.filter(user__id__in=friends_ids)
    my_profile=UserProfile.objects.get(user=request.user)
    
    friend_requests=FriendRequest.objects.filter(receiver=request.user)
    
    # users=Account.objects.all()
    context={'friends':friends,
             "friend_requests":friend_requests,
             "user_profiles":user_profiles,
             "my_profile":my_profile}
    return render(request, 'index.html', context)

def chat(request, id):
    user=Account.objects.filter(id=request.user.id)
    person=Account.objects.get(id=id)
    messages=Message.objects.filter(Q(sender=request.user, receiver=person) | Q(sender=person, receiver=request.user)).order_by('date', 'time')    
    message_data=serialize("json", messages)
    user_data=serialize("json",user)
    context={'messages':message_data,
             'person_first_name':person.first_name,
             'person_last_name':person.last_name,
             'user':user_data}
    
    return JsonResponse(context)
def send_request(request, id):
    receiver=Account.objects.get(id=id)
    
    friend_request_exists=FriendRequest.objects.filter(sender=request.user,
                                                receiver=receiver,
                                                status=False)
    if friend_request_exists:
        return JsonResponse({"message":"Already Sent"})

    friend_request=FriendRequest.objects.create(sender=request.user,
                                                receiver=receiver,
                                                status=False)
    friend_request.save()
    if friend_request:
        return JsonResponse({"message":"Friend Request Sent Successfully"})
    else:
        return JsonResponse({"message":"Something Went Wrong"})


def search(request):
    search_data = request.GET.get('search')
    
    users=Account.objects.filter(Q(first_name__icontains=search_data) | Q(email__icontains=search_data)).exclude(id=request.user.id)
    current_user=request.user
    my_profile=UserProfile.objects.get(user=current_user)
    friend_requests=FriendRequest.objects.filter(receiver=current_user)

    # .value_list('friend', flat-True) will return a list of ids of users that are in the field named as friend in the Friend Model
    friends=Friend.objects.filter(user=current_user).values_list('friend', flat=True)
    # Case is used to define a condition here it says that if the user.id is in friends list (that is containing ids od frineds users) then return true
    users=users.annotate(is_friend=Case(When(id__in=friends, then=True),
                                        default=False,
                                        output_field=BooleanField()))
    
    user_profiles=UserProfile.objects.filter(user__in=users)
    context={
        "users": users,
        'current_user': current_user,
        'user_profiles': user_profiles,
        'my_profile': my_profile,
        'friend_requests': friend_requests        
    }
    return render(request, "search.html", context)

def accept_request(request, id):
    to_be_friend=Account.objects.get(id=id)
    friend=Friend.objects.create(user=request.user, friend=to_be_friend)
    friend.save()
    myfriend=Friend.objects.create(user=to_be_friend, friend=request.user)
    myfriend.save()
    friend_request=FriendRequest.objects.get(sender=to_be_friend, receiver=request.user)
    friend_request.delete()
    return redirect("index")
    
def unfriend(request, id):
    user=Account.objects.get(id=id)
    to_delete=Friend.objects.filter(Q(friend=request.user, user=user) | Q(friend=user, user=request.user))
    to_delete.delete()
    return redirect("index")
    