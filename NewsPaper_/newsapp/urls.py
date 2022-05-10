
from django.urls import path
from .views import (PostList, PostDetail, NewsCreate, NewsEdit, NewsDelete,
                    ArticleCreate, ArticleEdit, ArticleDelete, UserUpdateView, CategoryList,
                    add_subscribe)


urlpatterns = [
   path('', PostList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('user/', UserUpdateView.as_view(), name='user_update'),
    path('category/', CategoryList.as_view(), name='category'),
    path('subscribe/<int:pk>', add_subscribe, name='subscribe'),
]

