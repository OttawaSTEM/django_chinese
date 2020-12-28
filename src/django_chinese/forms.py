import requests
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field, HTML

from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm, SetPasswordForm, ResetPasswordKeyForm
from captcha.fields import CaptchaField

class AllauthSignupForm(SignupForm):
    captcha = CaptchaField(label='验证码信息')
    def __init__(self, *args, **kwargs):
        super(AllauthSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = u'电子邮箱'
        self.fields['username'].label = u'用户名'
        self.fields['password1'].label = u'密码'
        self.fields['password2'].label = u'再次输入密码'
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': u'输入电子邮箱'})
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': u'输入用户名'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': u'输入密码'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': u'再次输入密码'})

class AllauthLoginForm(LoginForm):
    captcha = CaptchaField(label='验证码信息')
    def __init__(self, *args, **kwargs):
        super(AllauthLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = u'电子邮箱'
        self.fields['password'].label = u'密码'
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': u'输入电子邮箱'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': u'输入密码'})

class AllauthResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(AllauthResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = u'电子邮箱'
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': u'输入电子邮箱'})

class AllauthResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(AllauthResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = u'输入新密码'
        self.fields['password2'].label = u'再次输入新密码'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': u'输入新密码'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': u'再次输入新密码'})

class AllauthChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(AllauthChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = u'输入新密码'
        self.fields['password2'].label = u'再次输入新密码'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': u'输入新密码'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': u'再次输入新密码'})

class AllauthSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(AllauthSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = u'输入新密码'
        self.fields['password2'].label = u'再次输入新密码'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': u'输入新密码'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': u'再次输入新密码'})

class ContactForm(forms.Form):
    from_email = forms.EmailField(label=u'您的邮件地址：', required=True)
    subject = forms.CharField(label=u'邮件标题：', required=True)
    message = forms.CharField(label=u'邮件内容：', widget=forms.Textarea, required=True)
    captcha = CaptchaField(label=u'验证码信息')

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('from_email'),
            Field('subject'),
            Field('message'),
            Field('captcha'),
            # HTML('<div class="form-group my-4"><div class="g-recaptcha" data-sitekey="{}"></div></div>'.format(settings.RECAPTCHA_PUBLIC_KEY)),
            # HTML('<div class="form-group my-4"></div>'),
            Submit('sent', u'提交', css_class='float-right'),
        )