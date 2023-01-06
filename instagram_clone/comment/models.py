from django.db import models
from notification.models import Notification
from post.models import Post
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete

# Create your models here.

class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def user_comment(sender,instance,*args,**kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user

        notify = Notification(post=post,sender=sender,user=post.user,text_preview=text_preview,notification_type=2)
        notify.save()

    def user_delete_comment(sender,instance,*args,**kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user

        notify = Notification.objects.filter(post=post,sender=sender,user=post.user,text_preview=text_preview,notification_type=2)
        notify.delete()


    def __str__(self):
        return f'{self.user} commented on {self.post.user}\'s post.'

# For Comment
post_save.connect(Comment.user_comment,sender=Comment)

# For Comment Delete
post_delete.connect(Comment.user_delete_comment,sender=Comment)