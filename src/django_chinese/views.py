import sys, requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views import generic

from . import forms
from .utils import SendEmail

class HomePage(generic.TemplateView):
    template_name = 'home.html'

class AboutPage(generic.TemplateView):
    template_name = 'about.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        try:
            kwargs['contact_form'] = forms.ContactForm()
            return super(AboutPage, self).get(request, *args, **kwargs)
        except:
            messages.error(request, f'显示关于错误 - {sys.exc_info()}')
            return redirect('home')

    def post(self, request, *args, **kwargs):
        try:
            contact_form = forms.ContactForm(request.POST)
            if contact_form.is_valid():
                message = '邮件来自：{}\n{}'.format(contact_form.cleaned_data['from_email'], contact_form.cleaned_data['message'])
                SendEmail(subject=contact_form.cleaned_data['subject'], message=message)
                messages.success(request, '邮件已发送!')
                return HttpResponseRedirect('/about')
            else:
                messages.error(request, '验证码错误，请重新填写。')
                return super(AboutPage, self).get(request, contact_form=contact_form)
        except:
            messages.error(request, f'填写邮件信息错误！- {sys.exc_info()}')
            return redirect('home')
