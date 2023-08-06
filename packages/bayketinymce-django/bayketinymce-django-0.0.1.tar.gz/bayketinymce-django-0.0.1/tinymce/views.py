from typing import Any
from django.http.response import JsonResponse, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
# Create your views here.

class TinyMCEImageUpload(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': '未登录，请登录后操作！'}, json_dumps_params={'ensure_ascii': False})

        file = request.FILES.get('file')
        # 采用默认的store来保存文件
        path = default_storage.save(file.name, file)
        return JsonResponse({'location':default_storage.url(path)})