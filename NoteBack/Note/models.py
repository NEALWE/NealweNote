from django.db import models
import django.utils.timezone as timezone
from django.db import models
import pytz
from datetime import datetime
from django.conf import settings


class User(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    level = models.CharField(max_length=50, default='normal')
    mail = models.CharField(max_length=50, default='')
    phonenumber = models.CharField(max_length=50, default='')
    add_time = models.CharField(max_length=60, default='')
    update_time = models.CharField(max_length=60, default='')
    last_login_time = models.CharField(max_length=60, default='')
    last_login_ip = models.CharField(max_length=20, default='0.0.0.0')
    login_counts = models.IntegerField(default=0)


def md5(str_a):
    import hashlib
    # 创建md5对象
    m = hashlib.md5()
    # Tips
    # 此处必须encode
    # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
    # 因为python3里默认的str是unicode
    # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
    b = str(str_a)
    m.update(b)
    return m.hexdigest()


class Label(models.Model):
    cid = models.IntegerField(null=False)
    label_name = models.CharField(max_length=60, null=False)
    pid = models.IntegerField(default=0)


class Note(models.Model):
    note_id = models.IntegerField(null=False, default=10000, unique=True)
    note_tree_label = models.CharField(max_length=60, default='')
    note_title = models.CharField(max_length=60, default='')
    note_content = models.TextField(default='')
    add_time = models.CharField(max_length=60, null=False)

    # label = models.ForeignKey('Label', on_delete=models.CASCADE)


class NoteHistory(models.Model):
    note_title = models.CharField(max_length=60, default='')
    note_content = models.TextField(default='')
    label = models.ForeignKey('Label', on_delete=models.CASCADE)
    add_time = models.CharField(max_length=60, null=False)

    note = models.ForeignKey('Note', on_delete=models.CASCADE)


class File(models.Model):
    file_name = models.CharField(max_length=60, null=False)
    add_time = models.CharField(max_length=60, null=False)


class Tree(models.Model):
    username = models.CharField(max_length=60, null=False, default='nealwe', unique=True)
    tree_content = models.TextField(default='')
    add_time = models.CharField(max_length=60, null=False)