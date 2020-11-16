# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
import json
from itertools import groupby

from datetime import datetime
import random


class Index(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class News(View):
    def get(self, request, link: int):
        with open(settings.NEWS_JSON_PATH, "r") as f:
            posts = json.load(f)
            for i, post in enumerate(posts):
                if post["link"] == link:
                    return render(request, "news/index.html", context={"post": post})


class NewsMain(View):
    def get(self, request):
        search = request.GET.get("q", None)
        with open(settings.NEWS_JSON_PATH, "r") as f:
            posts = json.load(f)
            posts.sort(key=lambda x: x["created"], reverse=True)

            if search:
                articles = []
                for i, post in enumerate(posts):
                    if search in post["title"]:
                        articles.append(post)
            else:
                articles = posts

            groups = [{"date": key, "articles": list(group)} for key, group
                         in groupby(articles, key=lambda x: x["created"][:10])]

        return render(request, "news/news_main.html", context={"posts": groups})

class NewNews(View):

    def get(self, request):
        return render(request, "news/new_news.html")


    def post(self, request):



        with open(settings.NEWS_JSON_PATH, "r") as f:
            posts = json.load(f)

            links =[]
            link_num = round(random.random()) * 100
            for post in posts:
                links.append(post["link"])

            while link_num in links:
                link_num = round(random.random()) * 100

            new_post = {"created": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "text": request.POST.get('text'),
                        "title": request.POST.get('title'),
                        "link": str(link_num) }
            posts.append(new_post)

        with open(settings.NEWS_JSON_PATH, "w") as f:
            json.dump(posts, f)

        return redirect("/news/")


    # {"created": "2020-02-09 14:15:10", "text": "Text of the news 1", "title": "News 1", "link": 1}
