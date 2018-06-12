from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .sync_tools import algo_sync_tool

def home(request):
    params = {"items":["algo_sync_tools","interface_test"]}
    return render(request,'xiezhiai_test/home.html',context=params)

def algo_sync_tools(request):
    context = {}
    return render(request,'xiezhiai_test/algo_sync_tools.html',context)

def algo_sync_tool_result(request):
    line = []
    params = {}
    with open("log.txt","w") as file:
        file.truncate()
    print(request.POST["src_url"])
    request.POST["dst_url"]
    algo_sync_tool.start_copy(int(request.POST["src_url"]),int(request.POST["dst_url"]),int(request.POST["src_tid"]),int(request.POST["dst_tid"]),int(request.POST["choose"]))
    with open("log.txt") as file:
        line = file.readlines()
    print(line)
    params = {'lines':line}

    request.META["CSRF_COOKIE_USED"] = True
    return render(request,'xiezhiai_test/result_algo.html',context=params)

def interface_test(request):
    context = {}
    return render(request,'main/interface_test',context)

def interface_test_result(request):
    params = {}
    request.META["CSRF_COOKIE_USED"] = True
    return render(request, 'xiezhiai_test/result_interface.html', context=params)
