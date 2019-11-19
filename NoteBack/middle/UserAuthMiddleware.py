from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_login(request):
    try:
        if not request.session['is_login']:
            print("is_not_login")
            return False
        else:
            print("is_login")
            return True
    except:
        return False


class AuthMiddleware(MiddlewareMixin):


    def process_request(self, request):
        
        no_need_login = ['/', '/#/login', '/api/note/login/']

        if request.path not in no_need_login:
            if not is_login(request):
                return HttpResponseRedirect('/#/login')
            else:
                print(get_ip(request))
                return None
        else:
            return None

