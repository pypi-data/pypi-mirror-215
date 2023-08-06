# bayketinymce

## 安装配置

### 安装

```python
pip install bayketinymce-django
```

### 配置

1、在django项目配置文件settings文件中的INSTALLED_APPS注册app,并设置图片上传保存路径

```python
INSTALLED_APPS = [
    ...
    'tinymce',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

2、上传图片配置

在django项目的根urls.py中引入以下url

```python
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from tinymce.views import TinyMCEImageUpload

urlpatterns = [
    path('admin/', admin.site.urls),
    # 富文本编辑器上传图片url
    path("tinymce/upload-image/", TinyMCEImageUpload.as_view(), name="tinymce-upload-image")
]

# 开发环境下配置静态文件URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 快速使用

### 在models中使用

```python
from tinymce.fields import TinyMCEField

class Article(models.Model):
    content = TinyMCEField()
```

### 在forms表单中中使用

```python
# forms.py
from django import forms
from tinymce.forms import TinyMCEField
from tinymce.widgets import TinyMCEWidget

class TinyMCEForm(forms.Form):

    content = TinyMCEField(label="详情")

    or

    content = forms.CharField(widget=TinyMCEWidget(
            attrs={"class": 'input'}, tinymce_config={'menubar': False}
        )
    )
```

本项目所有的富文本编辑器相关均依赖 TinyMCEWidget 小部件，可以通过定制修改其参数tinymce_config的值（字典）来设置对应的富文本配置，具体配置项请参考tinymce官方配置文档，不支持配置js的方法及函数，仅支持 配置其值为字符串或数组及键值对对象的配置项！

### 修改默认富文本编辑器配置

在项目的settings.py中引入 TINYMCE_CONFIG 配置，该值是一个字典！

```python
TINYMCE_CONFIG = {
    # 是否开启富文本编辑器菜单,默认关闭，这里的配置会覆盖掉默认配置
    'menubar': False,
}
```
