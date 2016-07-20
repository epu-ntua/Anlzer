from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Project, User, Report
from django.http import Http404
from django.core.exceptions import PermissionDenied

# A quick lambda decorator for checking if the user is already logged in
anonymous_required = user_passes_test(lambda u: u.is_anonymous(), '/anlzer/projects')

def is_project_owner(viewfunc):
    """
    A decorator for checking whether the current user is the owner of the content
    based on the <pk> of the URL regex parameter
    """
    def check_and_call(request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        if not (project.user_id == request.user.pk or request.user.is_superuser):
            raise PermissionDenied

        return viewfunc(request, *args, **kwargs)

    return check_and_call


def is_project_participant(viewfunc):
    """
    A decorator for checking whether the current user is a member of the company
    that created the Project. Thus, whether he can manage its reports
    """
    def check_and_call(request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        if not (project.user == request.user or project.user == request.user.extra_data.under_company or request.user.is_superuser):
            raise PermissionDenied

        return viewfunc(request, *args, **kwargs)

    return check_and_call


def is_report_owner(viewfunc):
    """
    A decorator for checking whether the current user is the owner of the report
    """
    def check_and_call(request, *args, **kwargs):
        try:
            report = Report.objects.get(pk=kwargs['report_pk'])
        except Report.DoesNotExist:
            raise Http404("Report does not exist")

        if not (report.user == request.user or request.user == report.user.extra_data.under_company or request.user.is_superuser):
            raise PermissionDenied

        return viewfunc(request, *args, **kwargs)

    return check_and_call


def is_company(viewfunc):
    """
    A decorator for checking whether the current user is a company
    """
    def check_and_call(request, *args, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied

        return viewfunc(request, *args, **kwargs)
    return check_and_call


def is_account_owner(viewfunc):
    """
    A decorator for checking the currently logged in account
    has permission to delete the aforementioned account who's id
    derives from the URL regex variable <pk>
    """
    def check_and_call(request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            raise Http404("User ID does not exist")
        if not (user.extra_data.under_company == request.user or user == request.user or request.user.is_superuser):
            raise PermissionDenied

        return viewfunc(request, *args, **kwargs)
    return check_and_call

