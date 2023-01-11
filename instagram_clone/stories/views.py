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



def delete_story(request,story_id):
    story = Story.objects.get(id=story_id)
    story.delete()
    return redirect('index')