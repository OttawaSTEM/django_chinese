import os, uuid
from io import BytesIO
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible
from PIL import Image

from django_chinese.constants import PROVINCE


@deconstructible
class UploadStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super(UploadStorage, self).__init__(location=settings.MEDIA_ROOT, base_url='/media/')

def upload_to(instance, filename):      # Convert to (private) path, not full private yet
    profile_img = 'users/{}/profile_pics/{}'.format(instance.user.profile.slug, 'avatar.png')
    profile_img_path = os.path.join(settings.MEDIA_ROOT, profile_img)
    if os.path.exists(profile_img_path):
        os.remove(profile_img_path)
    return profile_img


class BaseProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here with default values,
    # CharFiled and TextFiled discouraged to use null=True in Django, avoid two possible values for “no data”: null and the empty string
    # python manage.py makemigrations profiles --name AddProfileModels
    picture = models.ImageField('头像', upload_to=upload_to, storage=UploadStorage(), blank=True, null=True)
    bio = models.CharField('个人简介', max_length=200, blank=True)
    email_verified = models.BooleanField('电子信箱验证', default=False)
    phone_number = models.CharField('联系电话', max_length=20, blank=True)
    school = models.CharField('所在学校', max_length=100, blank=True)
    address = models.CharField('通讯地址', max_length=100, blank=True)
    city = models.CharField('城市', max_length=30, blank=True)
    province = models.CharField('省份', max_length=12, blank=True, db_index=True, choices=PROVINCE)
    post_code = models.CharField('邮编', max_length=7, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.picture:
            image = Image.open(BytesIO(self.picture.read()))
            image.thumbnail((140,140))
            output = BytesIO()
            image.save(output, format='PNG')
            output.seek(0)
            self.picture= InMemoryUploadedFile(output, 'ImageField', '{}.png'.format('avatar'), 'image/png', len(output.getvalue()), None)
        super(BaseProfile, self).save(*args, **kwargs)


class Profile(BaseProfile):
    def __str__(self):
        return f'{self.user} - 个人资料'
