from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import NewPostForm
from .models import Follow, Post, PostFileContent,Stream,Tag,Likes
from app_auth.models import Profile
from django.http import HttpResponseRedirect
from comment.models import Comment
from comment.forms import CommentForm
from django.urls import reverse
from django.db.models import Q
import datetime
from stories.models import Story,StoryStream
# Create your views here.

@login_required
def index(request):
    user = request.user

    # Own Stories

    own_stories = Story.objects.filter(user=user)
    for story in own_stories:
        difference = datetime.datetime.now(datetime.timezone.utc) - story.posted
        if difference.days >= 1:
            story.delete()
    
    if len(own_stories) != 0:
        own_stories = own_stories

    # Stories of following
    following = Follow.objects.filter(follower=user)
    usernames_of_following = []

    for x in following:
        usernames_of_following.append(x.following)
        
    
    stories =[]
    for x in usernames_of_following:
        y = StoryStream.objects.filter(user=user,following=x)
        if y:
            stories.append(y)
            
    for story in stories:
        for file in story:
            if file.story.all().count() == 0:
                story.delete()
            else:
                for content in file.story.all():
                    difference = datetime.datetime.now(datetime.timezone.utc) - content.posted
                    if difference.days >= 1 :
                        content.delete()

    if len(stories) != 0:
        stories = stories


    # Posts
    
    posts = Stream.objects.filter(user=user) 
    posts_ids = []
    for post in posts:
        posts_ids.append(post.post_id)
    
    post_items = (Post.objects.filter(id__in=posts_ids) | Post.objects.filter(user=request.user)).all().order_by("-posted")
    
    len_of_post_items = len(post_items)
    len_of_own_stories = len(own_stories)
    len_of_stories = len(stories)


    context = {
        "post_items":post_items,
        "len_of_post_items":len_of_post_items,
        "stories":stories,
        "own_stories":own_stories,
        "len_of_stories":len_of_stories,
        "len_of_own_stories":len_of_own_stories
    }
    return render(request,'post/index.html',context)


@login_required
def post_detail(request,post_id):
    user = request.user
    post = get_object_or_404(Post,id=post_id)
    saved = False
    liked = False

    if Likes.objects.filter(user=user,post=post).exists():
        liked=True

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=user)

        if profile.favorites.filter(id=post_id).exists():
            saved=True
    
    # Comments
    comments = Comment.objects.filter(post=post).order_by("-date")

    # Comment Form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post_details', args=[post_id]))
    else:
        form=CommentForm()


    context={
        "post":post,
        'saved':saved,
        'liked':liked,
        "comments":comments,
        'form':form,
    }

    return render(request,'post/post_detail.html',context)

@login_required
def tags(request):
    tags = Tag.objects.all().annotate(posts_count=Count('tags')).order_by('-posts_count')
    context={
        "tags":tags,
    }
    return render(request,"post/tags.html",context)

@login_required
def tag_posts(request,tag_slug):
    tag = Tag.objects.filter(slug=tag_slug).first()
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    context = {
        "posts":posts,
        'tag':tag,
    }
    return render(request,'post/tag_posts.html',context)

@login_required
def new_post(request):
    user= request.user
    files_objects=[]
    if request.method == "POST":
        form = NewPostForm(request.POST,request.FILES)

        if form.is_valid():
            files=request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags = form.cleaned_data.get('tags')

            tags_list = list(tags.split(','))

            tags_objects_id = []
            for tag in tags_list:
                t , _ = Tag.objects.get_or_create(title=tag)
                tags_objects_id.append(t.id)

            for file in files:
                file_instance = PostFileContent(file=file,user=user)
                file_instance.save()
                files_objects.append(file_instance)

            p = Post.objects.create(caption=caption,user=user)
            p.tags.set(tags_objects_id)
            p.content.set(files_objects)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form':form,
    }

    return render(request,'post/new_post.html',context)

@login_required
def like(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    # Checking if the like exists for that post and user
    liked = Likes.objects.filter(user=user,post=post)

    if not liked:
        Likes.objects.create(user=user,post=post)
        current_likes += 1
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes -= 1
    post.likes = current_likes
    post.save()

    context={
        "liked":liked,
    }

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def save(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('index')

@login_required
def delete_comment(request,post_id,comment_id):
    comment = Comment.objects.get(id=comment_id)
    print(comment)
    comment.delete()
    return HttpResponseRedirect(reverse('post_details', args=[post_id]))


@login_required
def search_tag(request):
    query = request.GET.get('q')
    context = {}

    if query:
        tags = Tag.objects.filter(Q(title__icontains=query)|Q(slug__icontains=query)).annotate(posts_count=Count('tags')).order_by('-posts_count')
        context = {
            'tags':tags,
        }
    return render(request,'post/search_tag.html',context)