import logging
import json
from django.http.response import HttpResponse

from .utils.type_conversion import list_str

logger = logging.getLogger(__name__)


class MyBaseMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


class ResponseMiddleware(MyBaseMiddleware):
    """自定义返回结果"""

    def process_template_response(self, request, response):

        if hasattr(response, 'data'):
            # ============  返回详情  ============
            # {
            #     "code": "200",
            #     "message": "ok",
            #     "datas": { ... }
            # ============
            if response.status_code == 200:
                data = response.data
                if data:
                    if 'datas' not in response.data and 'code' not in response.data:
                        del response.data
                        response.data = {
                            'code': '{}'.format(response.status_code),
                            'message': 'ok',
                            'datas': data
                        }
                else:
                    response.data = {
                        'code': '{}'.format(response.status_code),
                        'message': 'ok',
                        'datas': data
                    }

            else:

                code = response.status_code
                response.status_code = 200
                response.data = {
                    'code': code,
                    'message': ';'.join(list(response.data.values())),
                    'datas': response.data,
                }

        return response


class CustomizeExceptionMiddleware(MyBaseMiddleware):
    """服务器异常不对外爆露，使用自定义"""

    def process_exception(self, request, exception):
        logger.error({'process_exception捕获异常': exception})

        return HttpResponse(
            json.dumps({'code': '06537',
                        'message': str(exception),
                        'datas': []
                        }),
            content_type="application/json")
