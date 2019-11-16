from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class AuthMiddleware(MiddlewareMixin):

    def is_login(self, request):
        try:
            if not request.session['is_login']:
                return False
            else:
                return True
        except:
            return False

    def process_request(self, request):
        need_login = ['/axf/mine/', '/axf/cart/']
        need_login_for_all = True

        if request.path in need_login or need_login_for_all:
            if not self.is_login:
                return HttpResponseRedirect('/#/login')
            else:
                print(get_ip(request))
                return None
        else:
            return None


