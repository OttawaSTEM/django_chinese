# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field, HTML

from . import models


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['username'].label = u'用户名称'
        self.helper.layout = Layout(Field('username'))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = [
            'bio', 'picture', 'phone_number', 'school', 'address', 'city', 'province', 'post_code'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('picture'),
            Field('bio'),
            Field('school'),
            Field('phone_number'),
            Field('address'),
            Field('city'),
            Field('province'),
            Field('post_code'),
            Submit('update', u'更新资料', css_class='btn-primary'),
        )
