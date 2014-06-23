from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

from .models import User


class RegistrationForm(forms.Form):
    """
    Form for registering a new account
    """
    email = forms.EmailField(label=_("Email"))
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))

    def clean_email(self):
        """
        Validate that the email doesn't already exist
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use."))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the passwords match
        """
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields do not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    user = None

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=self.data['email'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user
                else:
                    raise forms.ValidationError(_("This account is currently inactive."))
            else:
                raise forms.ValidationError(_("The user name and password you supplied is not valid."))

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            return True
        return False

