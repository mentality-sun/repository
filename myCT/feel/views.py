from django.shortcuts import render, redirect, HttpResponse
from feel import models


# Create your views here.
def regist(request):
    if request.method == "POST":
        # 获得表单数据
        a = request.POST.get("Username", None)
        b = request.POST.get("password", None)
        c = request.POST.get("Your Email", None)
        # d = request.POST.get("born", None)
        f = models.Regists.objects.filter(username=a)
        if f:  # 判断用户名是否已注册
            return render(request, 'signup.html')
        #         # 添加到数据库
        else:
            models.Regists.objects.create(
                username=a,
                password=b,
                email=c,

            )
        return redirect("/login/")
    return render(request, "signup.html")


def login(request):
    if request.method == 'POST':
        c = request.POST.get("Username", None)
        d = request.POST.get("password", None)
        # 对比输入的用户名和密码和数据库中是否一致
        models_User = models.Regists.objects.filter(username__exact=c, password__exact=d)
        if models_User:
            rep = redirect("/index/")
            rep.set_cookie("user", c, max_age=10)  # 存在时长十秒
            return rep
            # req.session['username'] = c
            # return redirect('/index/')
            # rep = redirect('/index/')
            # rep.set_cookie('username', c)
            # return rep
        else:
            message = "用户名或密码错误"
            return render(request, "login.html", {"msg": message})

    return render(request, 'login.html')


def index(request):
    return render(request, 'zhucaidan.html')


def caidan(request):
    # 分页操作
    current_page = request.GET.get('p', 1)
    ccc = int(current_page)
    print(ccc)
    start = (ccc - 1) * 10
    end = ccc * 10

    from django.utils.safestring import mark_safe  # xss安全机制
    # 将前端的用后端传入

    page = """
       <a href="/caidan/?p=1">1</a>
       <a href="/caidan/?p=2">2</a>
       <a href="/caidan/?p=3">3</a>"""
    # 安全机制1.在后端添加mark_safe(page)
    # 2.在前端添加“|safe”
    a = models.menu.objects.all()[start:end]
    return render(request, 'caidan123(1).html', {'s': a, "strpage": mark_safe(page)})


def pay(request):
    return render(request, 'pay.html')


def tianjia(request):
    if request.method == "GET":

        # img=models.caidan.objects.all()
        return render(request, 'shangchuan1.html')
    elif request.method == "POST":
        a = request.POST.get('ming', None)
        b = request.POST.get('price', None)
        obj = request.FILES.get("tu")
        #
        #         # f=open(obj.name,'wb')
        import os
        filepath = os.path.join("static", 'image0', obj.name)
        # f=open(os.path.join("upload",obj.name),'wb')
        # 将路径存入数据库

        f = open(filepath, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        # models.caixi.objects.create(path=filepath)
        if a:
            models.menu.objects.create(name=a, price=b, path=filepath)
        else:
            message = "不能空"
            return render(request, 'caidan123(1).html', {'msg': message})
        return redirect("/menu/")


def tijiao(request):
    if request.method == "POST":
        check_box_list = request.POST.getlist('tag')
        hnum = request.POST.get('fj', None)

        # import re
        # name = re.findall(r'name=(.*?)\d', "name=sd0price=asd'")
        # price = re.findall(r"price=(.*?)\'", "name=sd0price=asd'")
        # print(name, price)

        if check_box_list:
            import re
            list = []
            # ["name=sd0price=asd'", "name=fs0price=fs'"]
            print(check_box_list)
            for string in check_box_list:
                id = re.findall(r"id=(.*?)\'", string)[0]
                name = re.findall(r"name=(.*?)\'", string)[0]
                price = re.findall(r"price=(.*?)\'", string)[0]
                tupe = (id, name, price)

                list.append(tupe)
                a = [s[1] for s in list]
                b = [x[2] for x in list]
            print(list)
            for q in list:
                models.house.objects.create(

                    cname=q[1],
                    price=q[2],
                    hnumber=hnum,

                )
            return render(request, 'pay.html', {'list': list})
        else:
            print("fail")
            return HttpResponse("fail")
    else:  # [(asd,asda),(das,sad),(sad,asd)]
        a = [1, 2, 3, 4]
        return render(request, 'zhucaidan.html', {'a': a})


# def house(request):
#     if request.method=="POST"
import re
import time
import requests
import json

CURRENT_TIME = None
QCODE = None
LOGIN_COOKIE_DICT = {}
TICKET_COOKIE_DICT = {}
TIPS = 1


def log(request):
    base_qcode_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}'
    global CURRENT_TIME
    CURRENT_TIME = str(time.time())
    q_code_url = base_qcode_url.format(CURRENT_TIME)
    response = requests.get(q_code_url)
    print(response.text)
    # code代表二维码后缀
    code = re.findall('uuid = "(.*)";', response.text)[0]
    global QCODE
    QCODE = code
    return render(request, "log.html", {'code': code})


def long_polling(request):
    ret = {'status': 408, 'data': None}
    try:
        global TIPS
        base_login_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r=-1359574064&_={2}'
        login_url = base_login_url.format(QCODE, TIPS, CURRENT_TIME)
        response_login = requests.get(login_url)
        if "window.code=201" in response_login.text:
            TIPS = 0
            avatar = re.findall("userAvatar = '(.*)';", response_login.text)[0]
            ret['data'] = avatar
            ret['status'] = 201
        elif "window.code=200" in response_login.text:
            LOGIN_COOKIE_DICT.update(response_login.cookies.get_dict())
            redirect_uri = re.findall('redirect_uri="(.*)";', response_login.text)[0]
            redirect_uri += '&fun=new&version=v2&lang=ch_CN'
            response_ticket = requests.get(redirect_uri, cookies=LOGIN_COOKIE_DICT)
            TICKET_COOKIE_DICT.update(response_ticket.cookies.get_dict())

            # from bs4 import BeautifulSoup
            # print(ret.text)
            ret['status'] = 200
            print(response_login.text)
    except Exception as e:
        print(e)
        # print(ret.text)
    # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AxdM26O-4Tpw5rXOsU8deRNL@qrticket_0&uuid=QaFc68hL6w==&lang=zh_CN&scan=1534728899

    # print(response_login.text)
    return HttpResponse(json.dumps(ret))


def inde(request):
    return render(request, 'zhucaidan.html')


def a(request):
    a = models.house.objects.filter(hnumber=1)
    return render(request, 'show.html', {'list': a})


def b(request):
    b = models.house.objects.filter(hnumber=2)
    return render(request, 'show2.html', {'list2': b})


def c(request):
    c = models.house.objects.filter(hnumber=3)
    return render(request, 'show3.html', {'list3': c})


def d(request):
    d = models.house.objects.filter(hnumber=4)
    return render(request, 'show4.html', {'list4': d})


def e(request):
    e = models.house.objects.filter(hnumber=5)
    return render(request, 'show5.html', {'list5': e})


def f(request):
    f = models.house.objects.filter(hnumber=6)
    return render(request, 'show6.html', {'list6': f})


def g(request):
    g = models.house.objects.filter(hnumber=7)
    return render(request, 'show7.html', {'list7': g})


def h(request):
    h = models.house.objects.filter(hnumber=8)
    return render(request, 'show8.html', {'list8': h})


def house(request):
    return render(request, 'house.html')


def indexs(request):
    return render(request, "index.html")


def menu(request):
    # 分页操作
    current_page = request.GET.get('p', 1)
    ccc = int(current_page)
    print(ccc)
    start = (ccc - 1) * 10
    end = ccc * 10
    menu_list = models.menu.objects.all()[start:end]

    from django.utils.safestring import mark_safe  # xss安全机制
    # 将前端的用后端传入

    page = """
     <a href="/menu/?p=1">1</a>
     <a href="/menu/?p=2">2</a>
     <a href="/menu/?p=3">3</a>"""
    # 安全机制1.在后端添加mark_safe(page)
    # 2.在前端添加“|safe”

    return render(request, "menu.html", {'menu_lists': menu_list, "strpage": mark_safe(page)})


def fangjian(request):
    return render(request, 'fangjian.html')
