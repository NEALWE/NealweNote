import json
import time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('api_track')
logger_time = logging.getLogger('api_timeout')
logger_error = logging.getLogger("api_error")


class DataReCordMiddleware(MiddlewareMixin):
    def __init__(self, *args):
        super(DataReCordMiddleware, self).__init__(*args)
        self.start_time = None  # 访问时间
        self.end_time = None

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        time_obj = TimeUtils()
        now_time = time_obj.get_now_time()

        api = request.get_full_path()  # 1-获得请求的API
        request_method = request.method  # 2-获得请求的方法

        input_params = []  # 3-给请求参数一个默认值(空列表)
        user_id = "test"  # 4-给访问用户一个默认值

        if request_method == "GET":
            input_params = request.GET.dict()
            user_id = request.GET.get('user_id')
        elif request_method == "POST":
            input_params = request.POST.dict()
            user_id = request.POST.get('user_id')

        """
        elif request_method == "PUT":
            input_params = request.body.decode()
         '''
        """

        ret_dict = response.content.decode()  # 5-获得api返回的数据
        try:
            ret_dict = json.loads(ret_dict)  # 6-更改格式　这里之所以要try, 是因为返回404等界面时，不需要json.loads()
        except:
            pass

        logger.info("\n %s user_id = %s  api=%s  method=%s"  # 7-日志记录请求参数和返回结果
                    "\n %s input=%s "
                    "\n %s output=%s" % (
                    now_time, user_id, api, request_method, now_time, input_params, now_time, ret_dict))

        self.end_time = time.time()  # API响应时间
        waste_time = self.end_time - self.start_time  # 访问API消耗时间

        if waste_time >= 0.3:  # 这里可以自定义一个时间,作为耗时的标准, 超时的记录在一个日志文件中, 后期再对API进行优化
            logger_time.info('%s, 耗时:%s' % (api, waste_time))
        return response

    def process_exception(self, request, exception):
        api = request.get_full_path()
        ret = "服务器繁忙, 请稍后再试"
        logger_error.info("API: %s\n 异常信息:%s " % (api, exception))  # 还可以捕获异常, 写到错误日志里边, 测试阶段直接把exception返回就可以

        return JsonResponse({'code': -1, 'msg': '%s' % ret})
