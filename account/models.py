from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(_('first name'), max_length=1000)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=70, null=True, blank=True)
    temp_password = models.CharField(max_length=60, blank=True)
    initial_password_changed = models.BooleanField(default=False)
    initial_password_changed_at = models.DateTimeField(blank=True, null=True)

    @property
    def get_user_permissions_codenames(self):
        try:
            perms = Permission.objects.filter(content_type__app_label=User._meta.app_label,
                                              content_type__model=User._meta.model_name, user=self).order_by('codename')
            listp = list(set([x.codename for x in perms]))
        except:
            listp = []
        return ",".join(listp)

    @property
    def roles(self):
        return (str(self.get_user_permissions_codenames)).replace('_', ' ').title()
