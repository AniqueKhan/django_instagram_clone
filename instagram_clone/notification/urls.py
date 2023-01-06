from django.urls import path
from . import views
urlpatterns=[
    path('notifications',views.notifications,name='notifications'),
    path('<notification_id>/delete_notification',views.delete_notification,name='delete_notification'),
]