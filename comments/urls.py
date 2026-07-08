from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:news_id>/', views.add_comment, name='add_comment'),
]