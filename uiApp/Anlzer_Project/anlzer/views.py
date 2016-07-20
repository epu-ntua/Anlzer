from django.shortcuts import render, HttpResponse, render_to_response, get_object_or_404
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from .mixins import *
from .forms import *
from .classes import *
from django.utils.encoding import force_text
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.utils import timezone
from utils import SUPPORTED_LANGUAGES
import calendar
import json


class UserRegistrationView(CreateView):
    """
    A view for signing up a user in Anlzer
    """
    template_name = 'anlzer/account/register.html'
    form_class = UserCreationForm
    success_url = '/anlzer/projects'


class CompanyAdminPanelView(CreateView, AnlzerRequestMixin):
    """
    Class based view responsible for creating Individual Accounts for the Company.
    """
    template_name = 'anlzer/account/company-admin-panel.html'
    form_class = CompanyIndividualAccountForm
    success_url = '/anlzer/company/admin'

    @method_decorator(is_company)
    def dispatch(self, *args, **kwargs):
        return super(CompanyAdminPanelView, self).dispatch(*args, **kwargs)


class AccountDeleteView(AnlzerMessageMixin, DeleteView):
    """
    A class that takes care of the deletion of a Project.
    Performs confirmation on GET and deletion on POST
    """
    model = User
    template_name = 'anlzer/account/delete.html'
    success_message = "Your Account has been deleted !"
    success_url = '/anlzer/company/admin'

    @method_decorator(is_company)
    @method_decorator(is_account_owner)
    def dispatch(self, *args, **kwargs):
        return super(AccountDeleteView, self).dispatch(*args, **kwargs)


class ProjectCreationView(CreateView, AnlzerRequestMixin, IsCompanyMixin):
    """
    Class based view responsible for creating Projects.
    """
    template_name = 'anlzer/projects/create.html'
    form_class = ProjectForm

    def get_success_url(self):
        """
        Redirect based on the newly created <pk> of the Project
        """
        return "%s?new=True" % reverse('project-training', kwargs={'pk': self.object.pk})


class ProjectTrainingView(CreateView, AnlzerSingleProjectObjectMixin, IsProjectOwnerMixin, AnlzerProjectPkMixin):
    """
    Class based view responsible for creating a Training.
    """
    template_name = 'anlzer/projects/train.html'
    form_class = ProjectTrainingForm

    def get_success_url(self):
        """
        Redirect based on the newly created <pk> of the Project
        """
        return reverse('project', kwargs={'pk': self.kwargs['pk']})


class ProjectListView(ListView):
    """
    A view for displaying the projects of the user as a set of tiles
    """
    template_name = 'anlzer/projects/list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_company():
            return user.projects.all()
        else:
            return Project.objects.filter(user__in=[user, user.extra_data.under_company])


class ProjectUpdateView(AnlzerMessageMixin, UpdateView, AnlzerRequestMixin, IsProjectOwnerMixin):
    """
    A view for editing the Projects fields in the DB
    """
    template_name = 'anlzer/projects/update.html'
    model = Project
    form_class = ProjectForm
    success_message = "Project details have been updated successfully !"

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.kwargs['pk']})


class ProjectDeleteView(AnlzerMessageMixin, DeleteView, IsProjectOwnerMixin):
    """
    A class that takes care of the deletion of a Project.
    Performs confirmation on GET and deletion on POST
    """
    model = Project
    template_name = 'anlzer/projects/delete.html'
    success_message = "Your Project has been deleted !"

    def get_success_url(self):
        return reverse('projects')


class UserHomeView(ListView):
    """
    A view for displaying the Home Page of the registered User
    """
    template_name = 'anlzer/account/home.html'

    def get_queryset(self):
        qset = Project.objects.filter(user__in=[self.request.user, self.request.user.extra_data.under_company])
        return qset.order_by('-created_on')[:5]


class ReportCreationView(CreateView, AnlzerProjectPkMixin, AnlzerSingleProjectObjectMixin, AnlzerRequestMixin, IsProjectParticipantMixin):
    template_name = 'anlzer/reports/create.html'
    form_class = ReportForm

    def get_success_url(self):
        """
        Redirect based on the newly created <pk> of the Project
        """
        return "%s" % reverse('reports', kwargs={'pk': self.object.project_id})


class ReportUpdateView(AnlzerMessageMixin, UpdateView, AnlzerProjectPkMixin, AnlzerRequestMixin, IsReportOwnerMixin):
    template_name = 'anlzer/reports/update.html'
    form_class = ReportForm
    model = Report
    pk_url_kwarg = 'report_pk'
    success_message = "Report details have been updated successfully !"

    def get_success_url(self):
        """
        Redirect based on the newly created <pk> of the Project
        """
        return "%s" % reverse('reports', kwargs={'pk': self.object.project_id})


class ReportDeleteView(AnlzerMessageMixin, DeleteView, IsProjectParticipantMixin, IsReportOwnerMixin):
    """
    A class that takes care of the deletion of a Report.
    Performs confirmation on GET and deletion on POST
    """
    model = Report
    pk_url_kwarg = 'report_pk'
    template_name = 'anlzer/reports/delete.html'
    success_message = 'Your Report has been deleted !'

    def get_success_url(self):
        return reverse('reports', kwargs={'pk': self.object.project.pk})


class ReportListView(ListView, IsProjectParticipantMixin, AnlzerSingleProjectObjectMixin):
    """
    A view for displaying the reports of a Project of the user as a list of rows
    """
    template_name = 'anlzer/reports/list.html'

    def get_queryset(self):
        """
        Overrides the default query set of the <Report> class
        """
        pk = self.kwargs.get('pk', None)
        project = get_object_or_404(Project, pk=pk)
        return project.reports.all()


class ReportDetailView(DetailView, IsProjectParticipantMixin, AnlzerSingleProjectObjectMixin):
    """
    A view for displaying the details of a Report along with its menu
    """
    template_name = 'anlzer/reports/index.html'
    model = Report
    context_object_name = 'report'
    pk_url_kwarg = 'report_pk'

    def get_context_data(self, **kwargs):
        """
        Add languages to the context
        """
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['supported_languages'] = SUPPORTED_LANGUAGES
        return context



def index(request):
    return render(request, 'anlzer/landing/index.html', {})


@login_required
@is_project_owner
def project(request, pk=None):
    return render(request, 'anlzer/landing/index.html', {
        'project': Project.objects.get(pk=pk)
    })


@login_required
@is_project_owner
def download_training_file(request, pk):
    """
    Download one of the training files that the user has uploaded in the past
    """
    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    if request.method != 'GET':
        return HttpResponseForbidden('Only GET requests are allowed!')

    filename= request.GET.get('file', None)
    if not filename:
        return HttpResponseBadRequest('An error has occured on the download request!')

    relative_path = '%s/trainings/%s/%s' % (
        settings.MEDIA_ROOT,
        Project.objects.get(pk=pk).title,
        filename
    )

    filepath = os.path.join(settings.BASE_DIR, relative_path)
    wrapper = FileWrapper(open(filepath))
    content_type = mimetypes.guess_type(filepath)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
@is_project_participant
def get_project_sources(request, pk):
    """
    View that returns the sources of the chosen Project as a json serialized response
    """
    if request.method != 'GET':
        return HttpResponseForbidden('Only GET requests are allowed!')

    project = get_object_or_404(Project, pk=pk)
    payload = {
        'pages': project.pages,
        'hashtags': project.hashtags,
        'provider': [provider.pk for provider in project.provider.all()]
    }
    return JsonResponse(payload)

@login_required
def get_project_comments(request, pk):

    payload, project = [], get_object_or_404(Project, pk=pk)
    for comment in project.comments.all().order_by('-created_on'):
        payload.append({
            'id': comment.pk,
            'author': comment.author.username,
            'text': comment.message,
            'date': comment.created_on.strftime('%d %b %Y, %H:%M')
        })
    return JsonResponse(payload, safe=False)

@login_required
def post_project_comment(request, pk):
    Comment(
        author=request.user,
        project=Project.objects.get(pk=pk),
        message=request.POST['message']
    ).save()
    return HttpResponse('')


def get_report_details(request, pk, report_pk):

    project = get_object_or_404(Project, pk=pk)
    report = get_object_or_404(project.reports, pk=report_pk)

    json_object = {
        'pk': report_pk,
        'user': report.user.username,
        'title': report.title,
        'live': report.live,
        'live_range': report.live_range,
        'pages': report.pages.replace(' ', ''),
        'hashtags': report.hashtags.replace(' ', ''),
        'providers': ','.join([provider.name for provider in report.provider.all()]).replace(' ', '')
    }

    if report.live:
        live_days_dict = {
            'LAST_DAY': 1,
            'LAST_WEEK': 7,
            'LAST_MONTH': 30,
            'LAST_YEAR': 360
        }
        # what time is it now
        now = timezone.now()
        # initialize a value for the next live run. Subtract a second so that we have at least one "while" iteration
        closest_end = now + timedelta(seconds=10)
        closest_start = closest_end - timedelta(days=live_days_dict[report.live_range])

        # timetuple conversion
        json_object['start_date'] = calendar.timegm(closest_start.timetuple())
        json_object['end_date'] = calendar.timegm(closest_end.timetuple())

    else:
        json_object['start_date'] = calendar.timegm(report.start_date.timetuple())
        json_object['end_date'] = calendar.timegm(report.end_date.timetuple())

    return HttpResponse(json.dumps(json_object), content_type='application/json')
