'''
@file            :widgets.py
@Description     :表单组件
@Date            :2023/06/13 15:11:03
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

import json
from django.forms.widgets import Widget
from .config import get_tinymce_config, get_language

class TinyMCEWidget(Widget):

    template_name = "tinymce/editor.html"

    def __init__(self, attrs=None, tinymce_config=None) -> None:
        default_attrs = {"cols": "80", "rows": "10"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.tinymce_config = {**get_tinymce_config(), **(tinymce_config or {})}

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['tinymce_config'] = json.dumps(
            self.get_tinymce_config(attrs), ensure_ascii=False
        )        
        return context
    
    def get_tinymce_config(self, attrs):
        config = self.tinymce_config
        config['selector'] = f"textarea#{attrs['id']}"
        config['language'] = get_language()
        return config

    class Media:
        js = ['tinymce/tinymce.min.js',]