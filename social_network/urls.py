from django import views
from django.urls import path
from .views import token_user,register_user,user_connections,login_user, user_profile, create_post, view_post, like_post, comment_on_post, share_post, search_posts, user_connections

urlpatterns = [
    path('token_user/',token_user,name='token_user'),
    path('register/', register_user.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('profile/', user_profile, name='profile'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:post_id>/', view_post, name='view_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    # path('post/<int:post_id>/comment/', comment_on_post, name='comment_on_post'),
    path('post/<int:post_id>/share/', share_post, name='share_post'),
    path('posts/search/', search_posts, name='search_posts'),
    path('connections/', user_connections, name='user_connections'),
]
