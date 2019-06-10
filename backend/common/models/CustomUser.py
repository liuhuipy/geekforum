from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    company = models.CharField(max_length=64, blank=True, null=True, verbose_name='所在公司')