from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from news.models import News
from .models import Comment

@login_required
def add_comment(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                news=news,
                user=request.user,
                text=text
            )
    return redirect('news_detail', slug=news.slug)