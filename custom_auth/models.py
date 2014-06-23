from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        u = self.create_user(email, first_name, last_name, password, **extra_fields)
        u.is_admin = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser):
    email = models.EmailField(
        _('email address'),
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=255,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=255,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    is_admin = models.BooleanField(
        _('admin'),
        default=False,
        help_text=_('Designates whether this user should be treated as an admin.'),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'),
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
