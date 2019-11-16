# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from DarkWebTask.models import Loghistory, WeekReport

import logging
import json
import re
import datetime
from django.http import HttpResponse


def get_bj_time():
    utc_dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    bj_dt = utc_dt.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    return bj_dt


def get_ip(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip

class ApiLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.apiLogger = logging.getLogger('api')
        self.white_path_list = [
            '/darkwebmonitor/get_area_sum/',
            '/darkwebmonitor/get_sum_data/',
            '/darkwebmonitor/get_n_days_data/',
            '/darkwebmonitor/get_map_data/',
            '/darkwebmonitor/get_map_data/',
            '/darkwebmonitor/list_user/',
        ],
        self.download_path_list = [
            '/static/PublicUploads/'
        ],
        self.white_body_list = [
            "{'content': ''",
            "{'title': '', 'details': '', 'content_advance': '', 'province': '', 'city': '', 'person_name': '', 'start_date': '', 'end_date': '', 'delivery': '', 'content': ''"
        ]

    def body_check(self, body):
        for tmp_body in self.white_body_list:
            if tmp_body in str(body):
                return True
        return False

    def download_add(self, request):
        download_name = re.findall("static/PublicUploads/(.*?)", request.path)[0]
        if not WeekReport.objects.filter(file_name=download_name):
            return HttpResponse("LoginFirst!")
        download_times = WeekReport.objects.filter(file_name=download_name).values("download_times").first()[
                             'download_times'] + 1
        print(download_times)
        tmp = WeekReport.objects.filter(file_name=download_name).update(download_times=download_times)
        tmp.save()
        return 0

    def __call__(self, request):
        #检查下载文件的权限
        try:
            if str(self.download_path_list) in request.path and request.session['username'] == "":
                return HttpResponse("LoginFirst!")
            self.download_add(request)
        except:
            pass

        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()
        body.update(dict(request.POST))

        try:
            body.update(dict(request.POST))
            response = self.get_response(request)
            if request.path in str(self.white_path_list) or self.body_check(body):
                pass
            else:
                tmp = Loghistory(username=request.session['username'], method=request.method, path=request.path, body=body,
                           response_status_code=response.status_code, response_reason_phrase=response.reason_phrase, ip=get_ip(request), add_time=get_bj_time().strftime("%Y-%m-%d %H:%M:%S"))
                tmp.save()
                self.apiLogger.info("{} {} {} {} {} {}".format(
                    request.session['username'], request.method, request.path, body,
                    response.status_code, response.reason_phrase))
            return response
        except Exception as e:
            print(e)
            return response