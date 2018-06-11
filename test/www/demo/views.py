from django.shortcuts import render
from django.http import JsonResponse


# 通用页面
def hello(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'index.html', context)


# 主页
def home(request):
    return render(request, 'home.html')


def add(request):
    request.encoding = 'utf-8'
    if 'a' in request.GET:
        a = int(request.GET['a'])
    else:
        a = 0
    if 'b' in request.GET:
        b = int(request.GET['b'])
    else:
        b = 0
    c = a + b
    result = {'result': c}
    print(result)
    return JsonResponse(result)
