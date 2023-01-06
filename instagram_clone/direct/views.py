from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from app_auth.models import Profile
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct_profile = None
    active_direct = None
    directs = None

    if messages:
        message=messages[0]
        active_direct=message['user'].username
        active_direct_profile = get_object_or_404(Profile,user__username = active_direct)
        directs=Message.objects.filter(user=user,recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread']=0
    messages_count = len(messages)
    context={
        "messages_count":messages_count,
        "messages":messages,
        "active_direct":active_direct,
        "directs":directs,
        "active_direct_profile":active_direct_profile,
    }
    return render(request,'direct/direct.html',context)


@login_required
def direct(request,username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    active_direct_profile = get_object_or_404(Profile,user__username = username)
    directs = Message.objects.filter(user=user,recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username ==username:
            message['unread'] = 0
    
    context={
        "directs":directs,
        "messages":messages,
        "active_direct":active_direct,
        "active_direct_profile":active_direct_profile,
    }
    return render(request,'direct/direct.html',context)

@login_required
def send_direct(request):
    from_user = request.user
    to_user_username=request.POST.get("to_user")
    body = request.POST.get("body")

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user,to_user,body)
        return redirect('inbox')
    else:
        HttpResponseBadRequest()

@login_required
def search_user(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = Profile.objects.filter(Q(user__username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query))
        context = {
            'users':users,
        }
    return render(request,'direct/search_user.html',context)

@login_required
def new_conversation(request,username):
    from_user = request.user
    body = 'You started a conversation with {0}'.format(username)

    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search_user')
    
    # Restricting the user to send msgs to themselves
    if from_user != to_user:
        Message.send_message(from_user,to_user,body)

    return redirect('inbox')

def directs_count(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user,is_read=False).count()
    return {'directs_count':directs_count}