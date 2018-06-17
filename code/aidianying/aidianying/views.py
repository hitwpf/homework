from django.shortcuts import render
from django.http import JsonResponse
from .localCache import localCache
from .mvsearch import movieSearch
from .adjointthread import DaemonThread

# 伴随线程
daemonThread = DaemonThread()
daemonThread.start()


# 预加载推荐内容
def preload(films, start):
    count = len(films)
    for i in range(count):
        if i < start:
            continue
        film = films[i]
        title = film['title']
        daemonThread.enqueue(title)


# 网站主页
def home(request):
    return render(request, 'home.html')


def top(request):
    """
    首次进入页面，默认推送top5给用户
    """
    first = localCache.get(1)
    if first is None:
        first = movieSearch.search_2()
        if first is not None:
            data = []
            for film in first:
                temp = {'pic': film.coverUrl, 'title': film.title}
                data.append(temp)
            first = data
            localCache.add(1, first)
    result = {'code': -1}
    if first is not None:
        result['code'] = 0
        result['data'] = first
        preload(first, 0)
    return JsonResponse(result)


def lookup(request):
    """
    电影查询，最多返回六条数据，第一条是收索结果，其他5条是根据演员和导演关联查找的评分靠前的数据
    请求参数title，为电影名称，支持模糊查找，中英文有区别
    """
    request.encoding = 'utf-8'
    title = request.GET.get('title')
    if title is None:
        result = {'code': -2, 'msg': '非法请求'}
        return JsonResponse(result)
    title = title.strip()
    films = localCache.get(title)
    if films is None:
        films = movieSearch.search_1(title)
        data = []
        if films is not None:
            for film in films:
                data.append(film.toJson())
        localCache.add(title, data)
        films = data
    result = {'code': -1}
    if films is not None:
        result['code'] = 0
        result['data'] = films
        preload(films, 1)
        return JsonResponse(result)
