from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views import View
from operator import itemgetter
from json import load, dump
import datetime
import random
from django.shortcuts import redirect
# Create your views here.


class OldMainPageView(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse("<p>Coming soon</p>")
        return redirect("/news/")

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as f:
            news = load(f)
        q = None
        if request.GET.get('q'):
            q = request.GET.get('q')
        # if q:
        #     print(q, bool(q))
        news_sorted = sorted(news, key=itemgetter('created'), reverse=True)
        template = "<h2>Hyper news</h2>"
        i = 0
        if q:
            news_search = []
            for i, d in enumerate(news_sorted):
                if d["text"].lower().find(q.lower()) != -1 or d["title"].lower().find(q.lower()) != -1:
                    news_search.append(news_sorted[i])
            news_sorted = news_search
        # print(news_sorted)
        lastdate = datetime.datetime.strptime(news_sorted[0]["created"], "%Y-%m-%d %H:%M:%S")
        template += f"""<h4>{lastdate.date()} </h4>

<ul>"""
        for d in news_sorted:
            if datetime.datetime.strptime(d["created"], "%Y-%m-%d %H:%M:%S").date() != lastdate.date():
                lastdate = datetime.datetime.strptime(d["created"], "%Y-%m-%d %H:%M:%S")
                template += f"""</ul>
<h4>{lastdate.date()}</h4>

<ul>"""
            template += f"""
            <li><a href="/news/{d["link"]}/">{d["title"]}</a></li>
            """
        template += """</ul>
        <form action="/news" method="get">
        <input name="q">
        <button type="submit">search</button>
        </form>
        <a target="_blank" href="/news/create/">create</a>"""
        return HttpResponse(template)


class NewsPageView(View):
    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as f:
            news = load(f)
        # print(news, link)
        for d in news:
            # print(d["link"])
            if str(d["link"]) == link:
                template = f"""
                <h2>{d["title"]}</h2>
                <p>{d["created"]}</p>
                <p>{d["text"]}</p>
                <a target="_blank" href="/news/">news</a>
                """
                #print(template)
                return HttpResponse(template)
        raise Http404

class CreatePageView(View):
    with open(settings.NEWS_JSON_PATH, "r") as f:
        news = load(f)
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create/index.html')

# class SendPageView(View):

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = random.randrange(64000)
        self.news.append({"created": created, "text": text, "title": title, "link": link})
        with open(settings.NEWS_JSON_PATH, "w") as f:
            dump(self.news, f)
        return redirect("/news/")