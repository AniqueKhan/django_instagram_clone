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
	# path('password_change/', views.password_change, name='password_change'),
	# path('password_change/done', views.password_change_done, name='password_change_done'),
	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]