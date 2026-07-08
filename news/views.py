from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from banners.models import Banner
import json

from .models import News, Tag
from banners.models import Banner
from ticker.models import Ticker
from core.models import SiteSettings

def news_list(request):
    """Главная страница с лентой новостей"""
    news_list = News.objects.filter(is_active=True).order_by('-published_at')
    settings = SiteSettings.objects.first()

    # Поиск
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query)
        )

    left_banners = Banner.objects.filter(position='left', is_active=True).order_by('order')
    right_banners = Banner.objects.filter(position='right', is_active=True).order_by('order')
    headlines_count = settings.headlines_count if settings else 15
    recent_headlines = News.objects.filter(is_active=True).order_by('-published_at')[:headlines_count]

    ticker = Ticker.objects.filter(is_active=True).first()

    # Получаем и удаляем ID из сессии
    last_news_id = request.session.pop('last_news_id', None)

    promo_banner = Banner.objects.filter(position='center_top', is_active=True).order_by('order').first()

    return render(request, 'news/news_list.html', {
        'settings': settings,
        'news_list': news_list,
        'left_banners': left_banners,
        'right_banners': right_banners,
        'recent_headlines': recent_headlines,
        'ticker': ticker,
        'last_news_id': last_news_id,
        'promo_banner': promo_banner,
    })

def news_detail_pk(request, pk):
    news = get_object_or_404(News, pk=pk, is_active=True)
    # редирект на красивый URL
    return redirect('news_detail', slug=news.slug, permanent=True)

def news_detail(request, slug):
    """Страница отдельной новости по slug"""
    news = get_object_or_404(News, slug=slug, is_active=True)
    news.views_count += 1
    news.save(update_fields=['views_count'])

    request.session['last_news_id'] = news.pk

    settings = SiteSettings.objects.first()  # ← добавить
    left_banners = Banner.objects.filter(position='left', is_active=True).order_by('order')
    right_banners = Banner.objects.filter(position='right', is_active=True).order_by('order')
    recent_headlines = News.objects.filter(is_active=True).order_by('-published_at')[:15]
    ticker = Ticker.objects.filter(is_active=True).first()

    ticker = Ticker.objects.filter(is_active=True).first()

    return render(request, 'news/news_detail.html', {
        'news': news,
        'settings': settings,
        'left_banners': left_banners,
        'right_banners': right_banners,
        'recent_headlines': recent_headlines,
        'ticker': ticker,
    })

def banner_click(request, banner_id):
    """Обработчик кликов по рекламным баннерам"""
    banner = get_object_or_404(Banner, id=banner_id)
    banner.clicks_count += 1
    banner.save(update_fields=['clicks_count'])
    return redirect(banner.url)

def banner_view(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    banner.views_count += 1
    banner.save(update_fields=['views_count'])
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def toggle_reaction(request, news_id, emoji):
    """Добавить или убрать реакцию (доступно всем)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

    try:
        news = News.objects.get(id=news_id, is_active=True)
        data = json.loads(request.body)
        action = data.get('action', 'add')

        if action == 'add':
            news.add_reaction(emoji)
        else:
            news.remove_reaction(emoji)

        return JsonResponse({
            'success': True,
            'reactions': news.get_reactions()
        })
    except News.DoesNotExist:
        return JsonResponse({'error': 'Новость не найдена'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def news_view(request, news_id):
    news = get_object_or_404(News, id=news_id, is_active=True)
    news.views_count += 1
    news.save(update_fields=['views_count'])
    return JsonResponse({'status': 'ok'})


def news_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news_list = News.objects.filter(tags=tag, is_active=True).order_by('-published_at')
    
    return render(request, 'news/news_by_tag.html', {
        'tag': tag,
        'news_list': news_list,
    })