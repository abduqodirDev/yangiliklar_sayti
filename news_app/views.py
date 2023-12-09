from django.shortcuts import render, get_object_or_404
from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from config.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

# Create your views here.

def News_List(request):
    news_list=News.objects.filter(status=News.Status.Published)
    context={
        "news_list":news_list
        }
    return render(request, "news/news_list.html", context)



def News_Detail(request, news):
    news_detail=get_object_or_404(News, slug=news, status=News.Status.Published)
    context={}
    #hint_count log
    hit_count=get_hitcount_model().objects.get_for_object(news_detail)
    hits=hit_count.hits
    hitcontext=context['hitcount']={'pk':hit_count.pk}
    hit_count_response=HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits
    
    comments=news_detail.comments.filter(active=True)
    comment_count=comments.count()
    new_comment=None
    
    if request.method=='POST':
        comment_form=CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.news=news_detail
            new_comment.user=request.user
            new_comment.save()
      #      comment_form=CommentForm()
    else:
        comment_form=CommentForm()            
    context={
        "news_detail":news_detail,
        'comment_form':CommentForm,
        'comment_count':comment_count,
        'comments':comments
        }
    return render(request, "news/news_detail.html", context)



def ErrorPageView(request):
    return render(request, "news/404.html")



class ContactPageView(TemplateView):
    template_name="news/contact.html"
    
    def get(self, request, *args, **kwargs):
        form=ContactForm(),
        mashxur_xabarlar=News.published.all()[:5]
        contaxt={
            "form":form,
            "mashxur_xabarlar":mashxur_xabarlar
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
        context["comments"]=Comment.objects.all()[:4]
        context["category"]=Category.objects.all()
        context["news_list"]=News.published.all().order_by('-publish_time')[:5]
        context["ommabop"]=News.published.all().order_by('-publish_time')[5:10]
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
    
    
    
class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model=News
    fields=('title', 'body', 'image', 'category', 'status')
    template_name="crud/news_edit.html"
    
    
class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model=News
    template_name="crud/news_delete.html"
    success_url=reverse_lazy("index")
    
    
class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=News
    fields=("title", "title_uz", "title_ru", "title_en", "slug", "body","body_uz", "body_ru", "body_en", "image", "category", "status")
    prepopulated_fields={"slug":("title", )}
    template_name="crud/news_create.html"
    
    def test_func(self):
        return self.request.user.is_superuser
#   login_url="login"


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_user=User.objects.filter()
    news=News.objects.all()
    comment=Comment.objects.all()
    context={
        "admin_user":admin_user,
        "news":news,
        "comment":comment
        }
    
    return render(request, "pages/admin_page.html", context)


class SearchView(ListView):
    model=News
    template_name="news/search_news.html"
    context_object_name="barcha_yangiliklar"
    
    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
            )
    

class AboutView(TemplateView):
    template_name="news/about.html"
    
    
    
    



