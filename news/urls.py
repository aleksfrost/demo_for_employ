# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/view/<int:news_id>/', views.news_view, name='news_view'),
    path('banner/<int:banner_id>/', views.banner_click, name='banner_click'),
    path('react/<int:news_id>/<str:emoji>/', views.toggle_reaction, name='toggle_reaction'),
    path('banner/view/<int:banner_id>/', views.banner_view, name='banner_view'),
    path('tag/<slug:slug>/', views.news_by_tag, name='news_by_tag'),
]