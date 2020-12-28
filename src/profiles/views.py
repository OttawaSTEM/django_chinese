import os, shutil, sys
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from . import forms
from . import models

class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profiles/show_profile.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs.get('slug')
            if slug:
                profile = get_object_or_404(models.Profile, slug=slug)
                user = profile.user
            else:
                user = request.user

            if user == request.user:
                kwargs['editable'] = True

            kwargs['show_user'] = user
            return super(ShowProfile, self).get(request, *args, **kwargs)
        except:
            messages.error(request, f'Show profile error - {sys.exc_info()}')
            return redirect('home')


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profiles/edit_profile.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if 'user_form' not in kwargs:
                kwargs['user_form'] = forms.UserForm(instance=user)
            if 'profile_form' not in kwargs:
                kwargs['profile_form'] = forms.ProfileForm(instance=user.profile)
            
            return super(EditProfile, self).get(request, *args, **kwargs)
        except:
            messages.error(request, f'Show edit profile error - {sys.exc_info()}')
            return redirect('home')

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user_form = forms.UserForm(request.POST, instance=user)
            profile_form = forms.ProfileForm(request.POST, request.FILES, instance=user.profile)

            if not (user_form.is_valid() and profile_form.is_valid()):
                # messages.error(request, _('There was a problem with the form. Please check the details.'))
                message = 'Username: {}'.format(user_form.errors.get_json_data()['username'][0]['message'])
                messages.error(request, message)
                user_form = forms.UserForm(instance=user)
                profile_form = forms.ProfileForm(instance=user.profile)
                return super(EditProfile, self).get(request, user_form=user_form, profile_form=profile_form)
            
            # Both forms are fine. Time to save!
            user_form.save()
            profile = profile_form.save(commit=False)

            profile.user = user
            profile.save()  

            if not profile.picture:
                try:
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'users/{}/'.format(user.profile.slug)))
                except:
                    pass

            messages.success(request, u'个人资料已保存')
            return HttpResponseRedirect(reverse_lazy('profiles:show_self'))        
        except:
            messages.error(request, f'Post edit profile error - {sys.exc_info()}')
            return redirect('home')
