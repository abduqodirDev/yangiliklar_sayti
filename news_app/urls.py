from django.urls import path
from .views import (News_List,
                   News_Detail,
                   HomePageView,
                   ContactPageView,
                   ErrorPageView,
                   MahalliyPageView,
                   XorijPageView,
                   TexnologiyaPageView,
                   SportPageView,
                   NewsUpdateView,
                   NewsDeleteView,
                   NewsCreateView,
                   admin_page_view,
                   SearchView
                   )
urlpatterns=[
    path('', HomePageView.as_view(), name="index"),
    path('mahalliy/', MahalliyPageView.as_view(), name="mahalliy"),
    path('texnologiya/', TexnologiyaPageView.as_view(), name="texnologiya"),
    path('xorij/', XorijPageView.as_view(), name="xorij"),
    path('sport/', SportPageView.as_view(), name="sport"),
    path('news/', News_List, name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name="news_create"),
    path('news/<slug:news>/', News_Detail, name='news_detail'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name="news_edit"),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('error/', ErrorPageView, name='error'),
    path('admin_page/', admin_page_view, name="admin_page"),
    path('searchresult/', SearchView.as_view(), name="search_results")
    ]
