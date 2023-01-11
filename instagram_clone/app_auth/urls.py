from django.urls import path
from . import views

from django.contrib.auth import views as authViews 

urlpatterns = [
	path("<username>/",views.profile,name='profile'),
	path("editprofile",views.edit_profile,name='edit_profile'),
   path("<username>/saved",views.profile,name='saved'),
	path('<username>/follow/<option>',views.follow,name='follow'),
	path('signup', views.signup, name='signup'),
	path('login', authViews.LoginView.as_view(template_name='authentication/login.html'), name='login'),
	path('logout', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
]