'''
@file            :fields.py
@Description     :
@Date            :2023/06/13 14:52:57
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from typing import Any
from django.db.models.fields import TextField

from tinymce.widgets import TinyMCEWidget


class TinyMCEField(TextField):

    def formfield(self, **kwargs: Any) -> Any:
        kwargs['widget'] = TinyMCEWidget
        return super().formfield(**kwargs)