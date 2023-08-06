'''
@file            :config.py
@Description     :TinyMCE配置
@Date            :2023/06/14 15:22:56
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.conf import settings


TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons',
    'menubar': False,
    'toolbar1': 'undo redo | fontfamily fontsize blocks | searchreplace charmap emoticons removeformat fullscreen  preview  print code',
    'toolbar2': 'bold italic underline strikethrough link anchor alignleft aligncenter alignright alignjustify outdent indent numlist bullist forecolor backcolor insertfile codesample image media | autolink visualblocks visualchars ltr rtl',
    # 'toolbar': 'undo redo | bold italic underline strikethrough | fontfamily fontsize blocks | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media link anchor codesample | ltr rtl',
    # 'image_list': [
    #     { 'title': 'My image 1', 'value': 'https://www.example.com/my1.gif' },
    #     { 'title': 'My image 2', 'value': 'http://www.moxiecode.com/my2.gif' }
    # ],
    'toolbar_sticky': True,
    'image_advtab': True,
    # 'templates': [
    #     { 'title': 'New Table', 'description': 'creates a new table', 'content': '<div class="mceTmpl"><table width="98%%"  border="0" cellspacing="0" cellpadding="0"><tr><th scope="col"> </th><th scope="col"> </th></tr><tr><td> </td><td> </td></tr></table></div>' },
    #     { 'title': 'Starting my story', 'description': 'A cure for writers block', 'content': 'Once upon a time...' },
    #     { 'title': 'New list with dates', 'description': 'New List with dates', 'content': '<div class="mceTmpl"><span class="cdate">cdate</span><br><span class="mdate">mdate</span><h2>My List</h2><ul><li></li><li></li></ul></div>' }
    # ],
    'automatic_uploads': True,
    'images_upload_url': "/tinymce/upload-image/",
    'images_reuse_filename': True
}


TINYMCE_LANGUAGE_MAPS = {
    'zh-hans': 'zh-Hans',
    'en-us': 'en'
}

def get_tinymce_config():
    items = {}
    if hasattr(settings, 'TINYMCE_CONFIG'):
        items = { **TINYMCE_DEFAULT_CONFIG, **settings.TINYMCE_CONFIG }
    else:
        items = TINYMCE_DEFAULT_CONFIG
    return items

def get_language():
    return TINYMCE_LANGUAGE_MAPS.get(settings.LANGUAGE_CODE.lower(), 'zh-Hans')


