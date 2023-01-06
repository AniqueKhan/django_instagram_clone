from django.shortcuts import render,redirect
from .models import Notification
# Create your views here.

def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    notifications.update(is_seen=True)

    context = {
        "notifications":notifications,
    }

    return render(request,'notification/notifications.html',context)

def delete_notification(request,notification_id):
    user = request.user
    Notification.objects.filter(id=notification_id,user=user).delete()
    return redirect('notifications')

def count_notifications(request):
    count_notifications=0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user,is_seen=False).count()
    return {"count_notifications":count_notifications}
