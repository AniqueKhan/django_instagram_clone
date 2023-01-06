from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from post.models import Follow
from .forms import NewStoryForm
from .models import Story,StoryStream
# Create your views here.

def new_story(request):
    user = request.user

    if request.method == 'POST':
        form = NewStoryForm(request.POST,request.FILES)
        if form.is_valid():
            content = request.FILES.get('content')
            caption = form.cleaned_data.get('caption') 

            story = Story(user=user,content=content,caption=caption)
            story.save()
            return redirect('index')
    else:
        form = NewStoryForm()
    
    context ={
        'form':form,
    }
    return render(request,'stories/new_story.html',context)

def test(request):
    user=request.user
    following = Follow.objects.filter(follower=user)
    
    f = []
    
    for p in following:
        f.append(p.following)

    s = []
    for a in f:
        k=(StoryStream.objects.filter(user = user,following=a))
        if k:
            s.append(k)

    context={
        "following":following,
        "f":f,
        "s":s,
    }
    return render(request,'stories/test.html',context)


def delete_story(request,story_id):
    story = Story.objects.get(id=story_id)
    story.delete()
    return redirect('index')