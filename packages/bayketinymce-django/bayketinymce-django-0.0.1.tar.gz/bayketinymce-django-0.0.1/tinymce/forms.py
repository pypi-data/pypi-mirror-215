from django import forms
from tinymce.widgets import TinyMCEWidget
from tinymce.config import get_tinymce_config


class TinyMCEField(forms.CharField):

    widget = TinyMCEWidget

    