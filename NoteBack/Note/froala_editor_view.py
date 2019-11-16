# -*- coding: UTF-8 -*-
import json
# from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string


# Allow for a custom storage backend defined in settings.
def get_storage_class():
    return import_string(getattr(settings, 'FROALA_STORAGE_BACKEND', 'django.core.files.storage.DefaultStorage'))()


def md5_py3(str_a):
    '''
    python3
    :param str_a:
    :return:
    '''
    import hashlib
    # 创建md5对象
    m = hashlib.md5()
    # Tips
    # 此处必须encode
    # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
    # 因为python3里默认的str是unicode
    # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
    b = str(str_a)
    m.update(b.encode("utf8"))
    return m.hexdigest()


storage = get_storage_class()


def image_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/pjpeg',
            'image/x-png',
            'image/png',
            'image/gif'
        ]
        if not the_file.content_type in allowed_types:
            return HttpResponse(json.dumps({'error': _('You can only upload images.')}),
                                content_type="application/json")
        # Other data on the request.FILES dictionary:
        # filesize = len(file['content'])
        # filetype = file['content-type']

        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'static/uploads/froala_editor/images/')
        path = storage.save(os.path.join(upload_to, the_file.name), the_file)
        link = request.build_absolute_uri(storage.url(path))

        # return JsonResponse({'link': link})
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")


def file_upload(request):
    # 存在任意文件下载的问题
    try:
        if 'file' in request.FILES:
            # print(request.FILES)
            the_file = request.FILES['file']
            # print(the_file.name)
            upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'static/uploads/froala_editor/files/')
            path = storage.save(os.path.join(upload_to, md5_py3(the_file.name)), the_file)
            # print(path)
            link = storage.url(path)
            # print("storage.url(path):{link}".format(path=path, link=link))
            link = request.build_absolute_uri(storage.url(path))
            link = str(link).replace("/api/note/upload/static/uploads/", "/static/")
            link = str(link).replace("/note/upload/static/uploads/", "/static/")
            # print("request.build_absolute_uri(storage.url(path)): {link}".format(link=link))
            return HttpResponse(json.dumps({'link': link}), content_type="application/json")
    except Exception as e:
        print(e)

