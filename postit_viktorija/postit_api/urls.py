from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/comments/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('<int:pk>/like/', views.PostLike.as_view()),
    path('comment/<int:pk>/like/', views.CommentLike.as_view()),
    path('signup/', views.UserCreat.as_view()),
    path('die/', views.UserDelete.as_view()),
]

