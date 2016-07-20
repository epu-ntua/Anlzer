from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.contrib.auth import forms as auth_forms
from django.views.generic.edit import CreateView
import forms as anlzer_forms
from django.contrib.auth.decorators import login_required
from . import views
from .decorators import anonymous_required
from .forms import *


# Anlzer App patterns
app_name = 'anlzer'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),


    # Account specific pages
    #
    # These urls extend the Django's auth views/forms and thus they receive a lot of parameters
    # which could not be put easily in the views.py without having an intermediate view for passing them

    # Logs the user out
    url(r'^logout/$', login_required(auth_views.logout_then_login), name='logout'),

    # Registers the user in the platform
    url(r'^accounts/signup/$', anonymous_required(views.UserRegistrationView.as_view()), name='register'),

    # Logs the user in the platform
    url(r'^login/$', anonymous_required(auth_views.login),
        {
            'template_name': 'anlzer/account/login.html',
            'authentication_form': AnlzerAuthenticationForm
        },
        name='login'
    ),

    # Issues a password request where the user supplies his user email
    url(r'^accounts/password-reset/$', anonymous_required(auth_views.password_reset),
        {
            'template_name': 'anlzer/account/password-reset.html',
            'password_reset_form': AnlzerPasswordResetForm,
            'subject_template_name': 'anlzer/account/password-reset-subject.txt',
            'post_reset_redirect': 'done/',
            'email_template_name': 'anlzer/account/password-reset-email-content.html'
        },
        name='password-reset'
    ),

    # Displays success of password-reset email
    url(r'^accounts/password-reset/done/$', anonymous_required(auth_views.password_reset_done),
        {
            'template_name': 'anlzer/account/password-reset.html'
        },
        name='password-reset-done'
    ),

    # Tokenized url for the password reset
    url(r'^accounts/password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', anonymous_required(auth_views.password_reset_confirm),
        {
            'template_name': 'anlzer/account/password-reset-confirm.html',
            'set_password_form': AnlzerPasswordSetForm,
            'post_reset_redirect': '/accounts/password-reset/complete/'
        },
        name='password-reset-confirm'
    ),

    # Displays the outcome of the reset procedure
    url(r'^accounts/password-reset/complete/$', anonymous_required(auth_views.password_reset_complete),
        {
            'template_name': 'anlzer/account/password-reset-confirm.html'
        },
        name='password-reset-complete'
    ),

    # Deletes an account from the database
    url(r'^accounts/(?P<pk>\d+)/delete/$', login_required(views.AccountDeleteView.as_view()), name='account-delete'),

    # Alpha implementation of the Company's admin panel
    url(r'^company/admin/$', login_required(views.CompanyAdminPanelView.as_view()), name='company-admin-panel'),

    # Project specific pages
    #
    # 1. The pages that need a user to be logged in have the login_required decorator HERE
    # 2. pages that need a user to be the owner of the content, have a ProjectOwner mixin
    # in their class declaration. These are all the pages with the <pk> argument in their URL

    url(r'^$', login_required(views.UserHomeView.as_view()), name='home'),
    url(r'^projects/$', login_required(views.ProjectListView.as_view()), name='projects'),
    url(r'^projects/(?P<pk>\d+)/$', views.ReportListView.as_view(), name='project'), # Default view is a list of it's Reports
    url(r'^projects/create/$', login_required(views.ProjectCreationView.as_view()), name='project-create'),
    url(r'^projects/(?P<pk>\d+)/setup/$', views.ProjectUpdateView.as_view(), name='project-setup'),
    url(r'^projects/(?P<pk>\d+)/delete/$', views.ProjectDeleteView.as_view(), name='project-delete'),
    url(r'^projects/(?P<pk>\d+)/training/$', views.ProjectTrainingView.as_view(), name='project-training'),
    url(r'^projects/(?P<pk>\d+)/training/download/$', views.download_training_file, name='project-training-download'),

    # Report specific pages
    #
    # 1. The pages that need a user to be logged in have the login_required decorator HERE
    # 2. pages that need a user to be the owner of the content, have a ProjectOwner mixin
    # in their class declaration

    url(r'^projects/(?P<pk>\d+)/reports/$', views.ReportListView.as_view(), name='reports'),
    url(r'^projects/(?P<pk>\d+)/reports/(?P<report_pk>\d+)/$', views.ReportDetailView.as_view(), name='report'),
    url(r'^projects/(?P<pk>\d+)/reports/create/$', views.ReportCreationView.as_view(), name='report-create'),
    url(r'^projects/(?P<pk>\d+)/reports/(?P<report_pk>\d+)/update/$', views.ReportUpdateView.as_view(), name='report-update'),
    url(r'^projects/(?P<pk>\d+)/reports/(?P<report_pk>\d+)/delete/$', views.ReportDeleteView.as_view(), name='report-delete'),


    # Api views, that provide asynchronous data between client-server
    url(r'^api/projects/(?P<pk>\d+)/sources/$', views.get_project_sources, name='project-sources'),
    url(r'^api/projects/(?P<pk>\d+)/comments/$', views.get_project_comments, name='project-comments'),
    url(r'^api/projects/(?P<pk>\d+)/comments/post/$', views.post_project_comment, name='project-comment-post'),
    url(r'^api/projects/(?P<pk>\d+)/reports/(?P<report_pk>\d+)/$', views.get_report_details, name='api-report-details'),

    # Dummy urls not implemented yet
    url(r'^projects/(?P<pk>[0-9]+)/playground/$', views.project, name='project-playground'),
    url(r'^projects/reports/$', views.index, name='reports'),
    url(r'^projects/reports/$', views.index, name='report'),


]