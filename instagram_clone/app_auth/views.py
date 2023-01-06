from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import resolve , reverse
from post.models import Follow, Post , Stream
from .forms import EditProfileForm, SignupForm,ChangePasswordForm,ResetPasswordForm,ResetPasswordConfirmForm
from .models import Profile
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import uuid
from django.conf import settings

# Create your views here.


def sending_email(request,email,token):
	subject = 'Reset Link'
	msg = f'Hi ,click on this link to reset your password: \n {request.scheme}://{request.get_host()}/resetpasswordconfirm/{token}'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject,msg,email_from,recipient_list)
	return True

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('edit_profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'authentication/signup.html', context)


@login_required
def password_change(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('password_change_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'authentication/change_password.html',context)

def password_change_done(request):
	return render(request, 'authentication/change_password_done.html')

def reset_password(request):
	# if request.method == 'POST':
	# 	form = ResetPasswordForm(request.POST)
	# 	if form.is_valid():
	# 		email = request.POST.get('email')
	# 		user = User.objects.filter(email=email)
	# 		token = str(uuid.uuid4())
	# 		profile = Profile.objects.get(user__in=user)
	# 		profile.token_for_forgot_password = token
	# 		profile.save()
	# 		sending_email(request,email,token)
	# 		return redirect('reset_password_done')
	# else:
	# 	form = ResetPasswordForm()

	# context = {
	# 	'form':form,
	# }

	return render(request, 'reset_password.html', context)

def reset_password_done(request):
	return render(request, 'reset_password_done.html')

def reset_password_confirm(request,token):
	profile = Profile.objects.filter(token_for_forgot_password=token).first()
	if request.method=="POST":
		form = ResetPasswordConfirmForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			profile.user.set_password(new_password)
			profile.user.save()
			return redirect('reset_password_confirm_done')
	else:
		form = ResetPasswordConfirmForm()

	context = {
		'form':form,
	}

	return render(request, 'reset_password_confirm.html',context)

def reset_password_confirm_done(request):
    return render(request,'reset_password_confirm_done.html')

@login_required
def profile(request,username):
    user = get_object_or_404(User,username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by("-posted")
    
    else:
        posts = profile.favorites.all()
        posts.order_by("-posted")

	# Gathering follow status
    follow_status = Follow.objects.filter(follower=request.user,following=user)

    # Gathering Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

	
    context = {
        "profile":profile,
        "url_name":url_name,
        "posts":posts,
        "posts_count":posts_count,
        "following_count":following_count,
        "followers_count":followers_count,
		"follow_status":follow_status,
    }

    return render(request,'authentication/profile.html',context)

@login_required
def edit_profile(request):
	user = request.user.id
	profile =Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST,request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get("picture")
			profile.first_name = form.cleaned_data.get("first_name")
			profile.last_name = form.cleaned_data.get("last_name")
			profile.location = form.cleaned_data.get("location")
			profile.url = form.cleaned_data.get("url")
			profile.profile_info = form.cleaned_data.get("profile_info")
			profile.save()
			return redirect('profile',username=User.objects.get(id=user).username)
	else:
		form = EditProfileForm(instance=profile)
	
	context = {
		'form':form,
	}
	return render(request,'authentication/edit_profile.html',context)

@login_required
def follow(request,username,option):
    following = get_object_or_404(User,username=username)
    user = request.user

    try:
        f , _ = Follow.objects.get_or_create(follower=user,following=following)

        # Using 0 for unfollow
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following,user=user).all().delete()
        else:
            posts = Post.objects.filter(user=following)

            # Here we are just creating multiple Stream objects
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post,user=user,date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))
    except:
        return HttpResponseRedirect(reverse('profile',args=[username]))