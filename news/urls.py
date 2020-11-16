from django.urls import path
from .views import Index, News, NewsMain, NewNews

urlpatterns = [
    path('', NewsMain.as_view(), name="news_main"),
    path('<int:link>/', News.as_view(), name="news"),
    path('create/', NewNews.as_view(), name="new_news")
]
