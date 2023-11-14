from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

# Create your views here.

def News_List(request):
    news_list=News.objects.filter(status=News.Status.Published)
    context={
        "news_list":news_list
        }
    return render(request, "news/news_list.html", context)



def News_Detail(request, news):
    news_detail=get_object_or_404(News, slug=news, status=News.Status.Published)
    context={
        "news_detail":news_detail
        }
    return render(request, "news/news_detail.html", context)



def ErrorPageView(request):
    return render(request, "news/404.html")



class ContactPageView(TemplateView):
    template_name="news/contact.html"
    
    def get(self, request, *args, **kwargs):
        form=ContactForm()
        contaxt={
            "form":form
            }
        return render(request, "news/contact.html", contaxt)
    
    def post(self, request, *args, **kwargs):
        form=ContactForm(request.POST or None)
        if request.method=="POST" or form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur</h2>")
        context={
            "form":form
            }
        return render(request, "news/contact.html", context)
    
    
    
class HomePageView(ListView):
    model=News
    template_name="news/index.html"
    context_object_name="news"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["category"]=Category.objects.all()
        context["news_list"]=News.published.all().order_by('-publish_time')[:5]
        context["mahalliy_news"]=News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context["texnologiya_news"]=News.published.filter(category__name="Texnologiya").order_by('-publish_time')[:5]
        context["xorij_news"]=News.published.filter(category__name="Xorij").order_by('-publish_time')[:5]
        context["sport_news"]=News.published.filter(category__name="Sport").order_by('-publish_time')[:5]
        return context
    
    

class MahalliyPageView(ListView):
    model=News
    template_name="news/mahalliy.html"
    context_object_name="mahalliy"
    def get_queryset(self):
        news=self.model.published.filter(category__name="Mahalliy")
        return news



class XorijPageView(ListView):
    model=News
    template_name="news/xorij.html"
    context_object_name="xorij"
    def get_queryset(self):
        news=News.published.filter(category__name="Xorij")
        return news
   
    

class TexnologiyaPageView(ListView):
    model=News
    template_name="news/texnologiya.html"
    context_object_name="texnologiya"
    def get_queryset(self):
        news=News.published.filter(category__name="Texnologiya")
        return news



class SportPageView(ListView):
    model=News
    template_name="news/sport.html"
    context_object_name="sport"
    def get_queryset(self):
        news=News.published.filter(category__name="Sport")
        return news
    
    
    
    
    
    



