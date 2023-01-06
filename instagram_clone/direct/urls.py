from django.urls import path
from . import views
urlpatterns = [
    path("inbox",views.inbox,name='inbox'),
    path("direct/<username>",views.direct,name='direct'),
    path("send_direct",views.send_direct,name='send_direct'),
    path("search_user",views.search_user,name='search_user'),
    path("new_conversation/<username>",views.new_conversation,name='new_conversation'),
]