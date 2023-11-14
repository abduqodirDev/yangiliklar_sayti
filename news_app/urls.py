from django.urls import path
from .views import (News_List,
                   News_Detail,
                   HomePageView,
                   ContactPageView,
                   ErrorPageView,
                   MahalliyPageView,
                   XorijPageView,
                   TexnologiyaPageView,
                   SportPageView
                   )
urlpatterns=[
    path('', HomePageView.as_view(), name="index"),
    path('mahalliy/', MahalliyPageView.as_view(), name="mahalliy"),
    path('texnologiya/', TexnologiyaPageView.as_view(), name="texnologiya"),
    path('xorij/', XorijPageView.as_view(), name="xorij"),
    path('sport/', SportPageView.as_view(), name="sport"),
    path('news/', News_List, name='news_list'),
    path('news/<slug:news>/', News_Detail, name='news_detail'),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('error/', ErrorPageView, name='error')
    ]