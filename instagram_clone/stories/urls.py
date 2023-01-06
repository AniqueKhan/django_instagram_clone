from django.urls import path
from . import views

urlpatterns=[
    path('new_story',views.new_story,name='new_story'),
    path('delete_story/<story_id>',views.delete_story,name='delete_story'),
    path('test',views.test,name='test'),
]