from .models import News, Category
def latest_news(request):
    latest_news=News.published.all().order_by("-publish_time")[:10]
    category=Category.objects.all()
    context={
        "latest_news":latest_news,
        "category":category
        }
    return context
