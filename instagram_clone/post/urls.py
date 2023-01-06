from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('tags',views.tags,name='tags'),
    path('new_post',views.new_post,name='new_post'),
    path('post/<uuid:post_id>',views.post_detail,name='post_details'),
    path("search_tag",views.search_tag,name='search_tag'),
    path('post/<uuid:post_id>/like',views.like,name='like'),
    path('post/<uuid:post_id>/save',views.save,name='save'),
    path('post/<uuid:post_id>/delete',views.delete,name='delete'),
    path('post/<uuid:post_id>/comment/<uuid:comment_id>/delete',views.delete_comment,name='delete_comment'),
    path('tag/<slug:tag_slug>',views.tag_posts,name='tag_posts'),

]
   