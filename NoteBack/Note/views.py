from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q
from django.db.models import Sum,Count,Max,Min,Avg
from .models import Note, NoteHistory, Label, File, Tree, User
from .lib.pages import Pagination, PaginationQuery
from django.http import JsonResponse
from django.http import FileResponse
from django.core import serializers
import datetime
import os
import re
import json
import time
import csv


def safe_eval(string_tmp):
    env = {}
    env["locals"] = None
    env["globals"] = None
    env["__name__"] = None
    env["__file__"] = None
    env["__builtins__"] = None
    return eval(string_tmp, env)


# Create your views here.
def get_bj_time():
    utc_dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    bj_dt = utc_dt.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    return bj_dt


def get_ip(request):
    '''
    获取来源IP
    :param request:
    :return:
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def md5(str_a):
    import hashlib
    m = hashlib.md5()
    b = str(str_a)
    m.update(b.encode("utf8"))
    return m.hexdigest()


def byte_to_str(string):
    return str(string, encoding="utf-8")


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


def str_to_dict(string):
    return safe_eval(string)


def dict_to_json(tmp_dict):
    j = json.dumps(tmp_dict)
    return j


def module_path():
    """
    This will get us the program's directory
    """
    return os.path.dirname(os.path.realpath(__file__))


def login(request):
    start_time = time.time()
    postData = dict()
    postData['username'] = ''
    postData['password'] = ''
    postData = dict(postData, **json.loads(request.body.decode()))
    username = postData['username']
    password = postData['password']
    try:
        user_info = User.objects.filter(username=username, password=password)
        result = json.loads(serializers.serialize("json", user_info))
        if not result:
            return JsonResponse({'username': '', 'message': "用户名或者密码错误!"}, safe=False)
        username = result[0]['fields']['username']
        level = result[0]['fields']['level']
        request.session['is_login'] = True
        request.session['level'] = level
        request.session['username'] = username
        last_login_time = get_bj_time().strftime("%Y-%m-%d %H:%M:%S")
        last_login_ip = get_ip(request)
        last_login_counts = User.objects.filter(username=username).values("login_counts").first()['login_counts'] + 1
        User.objects.filter(username=username).update(last_login_time=last_login_time, last_login_ip=last_login_ip, login_counts=last_login_counts)
        request.session.set_expiry(60 * 60 * 1)
        return JsonResponse({'username': str(username), 'level': str(level)}, safe=False)
    except Exception as e:
        return JsonResponse({'username': '', 'message': "用户名或者密码错误!"}, safe=False)


def add_label(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_tree_label = postData['note_tree_label']
    add_time = get_bj_time()
    new_note_id = Note.objects.aggregate(Max("note_id"))['note_id__max']+1
    try:
        u1 = Note(note_id=new_note_id, note_tree_label=note_tree_label, note_title=note_tree_label, add_time=add_time)
        u1.save()
        return HttpResponse(new_note_id)
    except Exception as e:
        print(e)
        return HttpResponse("error")


def add_note(request):
    pass


def add_file(request):
    pass


def del_label(request):
    pass


def del_note(request):
    postData = dict()
    postData['note_id'] = ''
    postData['page'] = 1
    postData = dict(postData, **json.loads(request.body.decode()))
    note_id = postData['note_id']
    try:
        Note.objects.get(note_id=note_id).delete()
        return HttpResponse("{note_id} delete success!".format(note_id=note_id))
    except:
        return HttpResponse("{note_id} need to be created first!".format(note_id=note_id))
    pass


def del_file(request):
    pass


def update_label(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_id = postData['note_id']
    note_tree_label = postData['note_tree_label']
    # print(note_id)
    # print(note_tree_label)
    add_time = get_bj_time()
    try:
        if Note.objects.filter(note_id=note_id):
            if Note.objects.get(note_id=note_id).note_title == "testtest":
                Note.objects.filter(note_id=note_id).update(note_tree_label=note_tree_label, note_title=note_tree_label)
            Note.objects.filter(note_id=note_id).update(note_tree_label=note_tree_label)
        else:
            u1 = Note(note_id=note_id, note_tree_label=note_tree_label, note_title=note_tree_label, add_time=add_time)
            u1.save()
        return HttpResponse("update_label ok!")
    except:
        return HttpResponse("error update_label!")


def update_note(request):
    pass


def update_file(request):
    pass


def search(request):
    pass


def get_title(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_id = postData['note_id']
    try:
        if Note.objects.get(note_id=note_id):
            title = Note.objects.get(note_id=note_id).note_title
            return HttpResponse(title)
        else:
            return HttpResponse("")
    except:
        return HttpResponse("")

def get_label(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_id = postData['note_id']
    try:
        if Note.objects.get(note_id=note_id):
            note_tree_label = Note.objects.get(note_id=note_id).note_tree_label
            return HttpResponse(note_tree_label)
        else:
            return HttpResponse("Error note_tree_label")
    except:
        return HttpResponse("Error note_tree_label")


def get_note_content(request):
    start_time = time.time()
    # if not request.session['is_login'] or request.session['level'] != '管理员':
    #     return HttpResponse("LoginFirst!")
    postData = dict()
    postData['content'] = ''
    postData['page'] = 1
    postData = dict(postData, **json.loads(request.body.decode()))
    query = postData['content']
    page = postData['page']
    if query:
        data_list = Note.objects.filter(Q(note_title__contains=query)|Q(note_content__contains=query)|Q(note_tree_label__contains=query)).order_by('-add_time')
    else:
        data_list = Note.objects.all().order_by('-add_time')
    perPageCnt = 7  # 每页显示10个数据
    totalCnt = data_list.count()
    pageIndexCnt = 3  # 显示页码 5个
    if not page:
        page = 1
    currentPage = int(page)
    if query:
        pagination = PaginationQuery(currentPage, perPageCnt, totalCnt, pageIndexCnt, request.path, query)
    else:
        pagination = Pagination(currentPage, perPageCnt, totalCnt, pageIndexCnt, request.path)
    # 获取当前页面要显示的内容，使用切片模式
    if currentPage > 0 and currentPage < pagination.page_nums:
        data_list = data_list[pagination.startNum:pagination.endNum]
    elif currentPage == pagination.page_nums:
        data_list = data_list[pagination.startNum::]
    else:
        data_list = data_list[0:10]

    result = json.loads(serializers.serialize("json", data_list))
    result_tmp = {"data": result, "totalCnt": totalCnt, "pageSize": perPageCnt}
    # print(time.time() - start_time)
    # # print(result_tmp)
    return JsonResponse(result_tmp, safe=False)


def get_note_content_by_id(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_id = postData['note_id']
    try:
        if Note.objects.get(note_id=note_id):
            note_content = Note.objects.get(note_id=note_id).note_content
            return HttpResponse(note_content)
        else:
            return HttpResponse("")
    except:
        return HttpResponse("")


def getTree(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    username = postData['username']
    try:
        tree_content = Tree.objects.get(username=username).tree_content
        return JsonResponse({'tree_content': safe_eval(tree_content)}) # eval exist safe problem
    except Exception as e:
        return JsonResponse({'tree_content': ''})


def saveTree(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    username = postData['username']
    tree_content = postData['tree_content']
    add_time = get_bj_time()

    try:
        if Tree.objects.filter(username=username):
            Tree.objects.filter(username=username).update(tree_content=tree_content, add_time=add_time)
        else:
            u1 = Tree(username=username, tree_content=tree_content, add_time=add_time)
            u1.save()
    except:
        try:
            u1 = Tree(username=username, tree_content=tree_content, add_time=add_time)
            u1.save()
        except:
            return HttpResponse("Nope")
    return HttpResponse("saveTree ok")



def deal_tree_content(tree_content):
    for level_one in tree_content:
        if level_one['children'] != []:
            deal_tree_content(level_one['children'])
        else:
            add_time = get_bj_time()
            if Note.objects.filter(note_id=level_one['id']):
                Note.objects.filter(note_id=level_one['id']).update(note_tree_label=level_one['label'])
            else:
                u1 = Note(note_id=level_one['id'], note_tree_label=level_one['label'], add_time=add_time)
                u1.save()
    pass


def updateTree(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    username = postData['username']
    tree_content = postData['tree_content']

    try:
        deal_tree_content(tree_content)
    except:
        return HttpResponse("Error")
    return HttpResponse("updateTree ok")


def saveNodeContent(request):
    postData = dict()
    postData = dict(postData, **json.loads(request.body.decode()))
    note_title = postData['note_title']
    note_tree_label = postData['note_tree_label']
    note_content = postData['note_content']
    note_id = postData['note_id']
    add_time = get_bj_time()

    try:
        if Note.objects.filter(note_id=note_id):
            Note.objects.filter(note_id=note_id).update(note_title=note_title, note_content=note_content, add_time=add_time)
        else:
            u1 = Note(note_id=note_id, note_title=note_title, note_content=note_content, note_tree_label=note_tree_label, add_time=add_time)
            u1.save()
    except Exception as e:
        # print(e)
        try:
            u1 = Note(note_id=note_id, note_title=note_title, note_content=note_content, add_time=add_time)
            u1.save()
        except Exception as e:
            # print(e)
            return HttpResponse("Nope")
    return HttpResponse("saveNodeContent ok")


# def login(request):
#     postData = dict()
#     postData = dict(postData, **json.loads(request.body.decode()))
#     # print(postData)
#     return JsonResponse({"code": 20000, "data": {"token": "admin-token"}}, safe=False)


def upload(request):
    return HttpResponse("upload ok")

