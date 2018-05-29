# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from .models import  User
from django.core.exceptions import ValidationError
import re
def email_validate(value):
    mobile_re = re.compile(r'^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$')
    if not mobile_re.match(value):
        raise ValidationError('格式错误')

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),max_length=20,error_messages={"required": "password不能为空",})

class RegForm(forms.Form):
    '''
    注册表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),min_length=4,max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),max_length=50,error_messages={"required": "email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),min_length=4,max_length=20,error_messages={"required": "password不能为空",})

    def clean(self):

        #邮箱
        try:
            self.email = self.cleaned_data['email']
        except Exception as e:
            raise forms.ValidationError("需为邮箱格式")

        return self.cleaned_data

class CommentForm(forms.Form):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),max_length=50,error_messages={"required":"username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
                                                           "required":"required","size":"25", "tabindex":"2"}),max_length=50, error_messages={"required":"email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())


