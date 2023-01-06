from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from post.models import Follow

def user_directory_path(instance,filename):
    # The post pictures will be uploaded to MEDIA_ROOT/user_<id>/filename
    return 'user_{0}/{1}'.format(instance.user.id,filename)


# Create your models here.
class Story(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="story_user")
    content = models.FileField(upload_to=user_directory_path)
    caption = models.TextField(max_length=90)
    posted = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.user.username

class StoryStream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='story_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    story = models.ManyToManyField(Story, related_name='stories')
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Streamed to {self.user.username} by {self.following.username}'

    def add_story(sender,instance,*args,**kwargs):
        new_story = instance
        user = new_story.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            try:
                # Checking if the story stream already exists or not
                s = StoryStream.objects.get(user = follower.follower,following=user)
            except StoryStream.DoesNotExist:
                s = StoryStream.objects.create(user=follower.follower,date=new_story.posted,following=user)
            
            s.story.add(new_story)
            s.save()

# For Story Stream
post_save.connect(StoryStream.add_story,sender=Story)