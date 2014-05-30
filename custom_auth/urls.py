from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views
from custom_auth import views as auser_views

urlpatterns = patterns('',
    url(r'^login/$', auser_views.login, {'template_name': 'custom_auth/login.html'}, name='auth_login'),
    url(r'^logout/$', auser_views.logout, name='auth_logout'),
    url(r'^manage/$', auser_views.manage, name='auth_manage'),
    url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
    url(r'^profile/$', auser_views.profile, {'template_name': 'custom_auth/profile.html'}, name='auth_profile'),
    url(r'^register/$', auser_views.register, {'template_name': 'custom_auth/register.html'}, name="auth_register"),
    url(r'^register/successful/$', auser_views.registration_successful, {"template_name": "custom_auth/registration_successful.html"}, name="registration_successful")
)
