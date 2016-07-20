from django.views.generic.edit import CreateView, ProcessFormView, BaseCreateView, ModelFormMixin
from django.shortcuts import HttpResponse
from django import forms
from django.http.response import JsonResponse
from .models import Project
from django.views.generic.base import ContextMixin
from django.views.generic import View
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            safe=False,
            **response_kwargs
        )

    def get_data(self, context):
        """
        To be extended
        """
        return context


class AnlzerSingleProjectObjectMixin(ContextMixin):
    """
    A mixin that adds the currently active project
    taken from the url regex parameter <pk> to the
    context of the template
    """
    def get_context_data(self, **kwargs):
        """
        Get the current Project object, as a django template variable
        """
        context = super(AnlzerSingleProjectObjectMixin, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context


class AnlzerRequestMixin(ModelFormMixin):
    """
    Base Class that Anlzer Class based view will inherit when dealing with Project objects.
    It extends the current kwargs of the form that the class view refers to
    by adding the request object as a kwarg parameter of the form
    """
    def get_form_kwargs(self):
        kwargs = super(AnlzerRequestMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class AnlzerProjectPkMixin(ModelFormMixin):

    def get_form_kwargs(self):
        """
        Pass the <pk> of the current request (from the URL)
        to the form that will be initialized. <pk> is contained
        in the parameters of the current request (self.kwargs)
        """
        kwargs = super(AnlzerProjectPkMixin, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class FormFieldsClassMixin(forms.BaseForm):
    """
    A small mixin that accepts the parameter <class> parameter and appends it
    to the widgets of all fields of the class it extends
    """
    def __init__(self, *args, **kwargs):
        super(FormFieldsClassMixin, self).__init__(*args, **kwargs)
        _class = self.class_name if 'class_name' in self else 'input-lg'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = _class


class AnlzerAjaxPostMixin(BaseCreateView):
    """
    A simple mixin to handle AJAX POST(!) requests only. What it does is
    check the type of the request and returns an 'Ok' signal with 204 code
    if the form was valid, else the parsed html with the errors
    """
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None

        if form.is_valid():
            if request.is_ajax():
                form.save()
                return HttpResponse('Ok', status=204)
            return self.form_valid(form)

        else:
            return self.form_invalid(form)


class IsProjectOwnerMixin(View):
    """
    Mixin for checking whether the user has permission
    to do an action through ownership of content
    """
    @method_decorator(login_required)
    @method_decorator(is_project_owner)
    def dispatch(self, *args, **kwargs):
        return super(IsProjectOwnerMixin, self).dispatch(*args, **kwargs)


class IsCompanyMixin(View):
    """
    Mixin for checking whether the user is a company
    """
    @method_decorator(is_company)
    def dispatch(self, *args, **kwargs):
        return super(IsCompanyMixin, self).dispatch(*args, **kwargs)


class IsProjectParticipantMixin(View):
    """
    Mixin for checking whether the user has permission
    to do an action through his participation in a project
    """
    @method_decorator(login_required)
    @method_decorator(is_project_participant)
    def dispatch(self, *args, **kwargs):
        return super(IsProjectParticipantMixin, self).dispatch(*args, **kwargs)


class IsReportOwnerMixin(View):
    """
    Mixin for checking whether the user has permission
    to do an action through ownership of <Report> type content
    """
    @method_decorator(login_required)
    @method_decorator(is_report_owner)
    def dispatch(self, *args, **kwargs):
        return super(IsReportOwnerMixin, self).dispatch(*args, **kwargs)



class AnlzerMessageMixin(SuccessMessageMixin):
    """
    Extends Django's SuccessMessageMixin by adding the functionality of deleting
    rather than having it only work for form_valid
    """
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(SuccessMessageMixin, self).delete(request, *args, **kwargs)