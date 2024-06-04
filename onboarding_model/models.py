
from django.conf import settings
from .model_manager import ParentOnboardingUserManager
from django.contrib.auth.models import PermissionsMixin
import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class CommonTimePicker(models.Model):
    """
    An abstract model in Django that provides two fields, `created_at` and `updated_at`, which automatically record the date and time when an object is created or updated.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ParentOnboardingUser(AbstractBaseUser, PermissionsMixin, CommonTimePicker):
    PARENT_TYPE_CHOICES = (
        ('Mother', 'Mother'),
        ('Father', 'Father'),
    )
    EXPERIENCE_TYPE_CHOICES = (
        ('First-time', 'First-time'),
        ('Experienced', 'Experienced'),
    )

    user_type = models.CharField(max_length=10, choices=PARENT_TYPE_CHOICES)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_details = models.TextField()
    address = models.TextField()
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type', 'experience_type']

    objects = ParentOnboardingUserManager()

    def __str__(self):
        return f'{self.user_type}_{self.name}_{self.email}'

class Child(CommonTimePicker):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=255)
    age_in_months = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(240)])
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    gender = models.CharField(max_length=10, choices=gender_choices)

    def __str__(self):
        return f'{self.name}_{self.age_in_months}'

class BlogCategory(CommonTimePicker):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Blog(CommonTimePicker):
    title = models.CharField(max_length=255)
    content = models.TextField()
    categories = models.ManyToManyField(BlogCategory, related_name='blogs')
    parent_types = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogs', blank=True)
    age_group_start = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(240)])
    age_group_end = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(240)])
    gender_specific = models.CharField(max_length=10, choices=Child.gender_choices, blank=True, null=True)
    geolocation = models.CharField(max_length=255, blank=True, null=True, default = None) # Optional geolocation filter

    def __str__(self):
        return self.title

