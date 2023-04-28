from django.shortcuts import render

# Create your views here.

from news_api.models import newsdetail
from django.http import JsonResponse


def daily_news(request):
    return JsonResponse({'status': 200, 'data': [{
        'id': _.news_id,
        'title': _.title
    }
        for _ in newsdetail.objects.all().order_by('-date')[:5]
    ]})
