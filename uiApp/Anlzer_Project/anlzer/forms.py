from django.contrib.auth import forms as auth_forms
from .models import *
from django import forms
from .mixins import FormFieldsClassMixin
from unidecode import unidecode
from django.template.defaultfilters import slugify


class AnlzerAuthenticationForm(auth_forms.AuthenticationForm, FormFieldsClassMixin):
    """
    Extending for the Mixin
    """
    pass


class AnlzerPasswordResetForm(auth_forms.PasswordResetForm, FormFieldsClassMixin):
    """
    Extending for the Mixin
    """
    pass


class AnlzerPasswordSetForm(auth_forms.SetPasswordForm, FormFieldsClassMixin):
    """
    Extending for the Mixin
    """
    pass


class UserCreationForm(auth_forms.UserCreationForm, FormFieldsClassMixin):
    """
    A form that creates a user, overriding default auth/forms Form
    by requiring an email for the registration completion
    """
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta(auth_forms.UserCreationForm.Meta):
        fields = ['username', 'email']


class CompanyIndividualAccountForm(auth_forms.UserCreationForm, FormFieldsClassMixin):
    """
    A form that creates an individual user for the company by prompting the company
    to provide a username & password
    """
    def __init__(self, request, *args, **kwargs):
        super(CompanyIndividualAccountForm, self).__init__(*args, **kwargs)
        self.fields['password2'].required = False
        self.company = request.user

    def clean_password2(self):
        """
        Override default password-match-check since the company will only provide 1 password
        """
        return self.cleaned_data.get("password2")

    def save(self, commit=True):
        """
        Override "save" so we can assign this account under the specific company that created it
        """
        user = super(CompanyIndividualAccountForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        e = user.extra_data
        e.user_type = 'INDIVIDUAL'
        e.under_company = self.company
        e.save()

        return user


class ProjectForm(forms.ModelForm, FormFieldsClassMixin):
    """
    A form responsible for creating a new Project-object
    """
    error_messages = {
        'project_title_exists': "The project title you entered already exists.",
        'no_provider_selected': "You must select at least one service to search",
    }

    class Meta:
        model = Project
        exclude = ('user', 'created_on', 'slug',)

    def __init__(self, *args, **kwargs):
        """
        Extend the objects argument by requiring the request object on initialization

        If we are updating we keep a copy of the instance in self. We do not use .pop
        there because else we would lose the reference to the object being updated

        If we are not updating we are thus creating, so instance is None
        """
        self.request = kwargs.pop('request', None)
        self.instance_to_update = kwargs['instance'] if 'instance' in kwargs else None
        super(ProjectForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        """
        Checks whether the user already used this project title
        The 2nd if has to do with the updating. If self.instance is populated
        then we assume that the existing title already belongs to this instance
        so its fine to let it pass
        """
        title = self.cleaned_data.get("title")
        if self.request.user.projects.filter(title=title).exists():
            if not self.instance_to_update:
                raise forms.ValidationError(
                    self.error_messages['project_title_exists'],
                    code='project_title_exists'
                )
        return title

    def save(self, commit=True):
        """
        Adds the current user as owner of the project and creates a slug
        from the newly added title, before the actual saving
        of the Project-object in the database
        """
        project = super(ProjectForm, self).save(commit=False)
        project.user = self.request.user
        project.slug = slugify(unidecode(project.title))
        if commit:
            project.save()
            self.save_m2m()
        return project


class ReportForm(forms.ModelForm, FormFieldsClassMixin):
    """
    A form responsible for creating a new Project-object
    """
    error_messages = {
        'report_title_exists': "The report title you entered already exists.",
        'no_provider_selected': "You must select at least one service to search",
    }

    class Meta:
        model = Report
        exclude = ('project', 'status', 'created_on', 'slug', 'user',)

    def __init__(self, pk, request, report_pk=None, *args, **kwargs):
        """
        Extend the objects argument by requiring the request object on initialization

        If we are updating we keep a copy of the instance in self. We do not use .pop
        there because else we would lose the reference to the object being updated

        If we are not updating we are thus creating, so instance is None
        """
        self.project = Project.objects.get(pk=pk)
        self.instance_to_update = kwargs['instance'] if 'instance' in kwargs else None
        self.request = request

        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields['pages'].required = False

    def clean_title(self):
        """
        Checks whether the user already used this project title
        The 2nd if has to do with the updating. If self.instance is populated
        then we assume that the existing title already belongs to this instance
        so its fine to let it pass
        """
        title = self.cleaned_data.get("title")
        if self.project.reports.filter(title=title).exists():
            if not self.instance_to_update:
                raise forms.ValidationError(
                    self.error_messages['report_title_exists'],
                    code='project_title_exists'
                )
        return title

    def clean(self):
        return super(ReportForm, self).clean()

    def save(self, commit=True):
        """
        Adds the current user as owner of the project and creates a slug
        from the newly added title, before the actual saving
        of the Project-object in the database
        """
        report = super(ReportForm, self).save(commit=False)
        report.project = self.project
        report.user = self.request.user
        report.slug = slugify(unidecode(report.title))
        report.pages = report.pages if report.pages else '*'

        if report.live:
            report.start_date = report.end_date = None

        if commit:
            report.save()
            self.save_m2m()
            
        return report


class ProjectTrainingForm(forms.ModelForm, FormFieldsClassMixin):
        """
        A form responsible for uploading a Training file on a specific project
        """
        def __init__(self, pk, *args, **kwargs):
            """
            Get the <pk> from the URL REGEX parameters and store the project
            with that <pk> in the current object (self) so we can assign the uploaded
            file to THAT project in the save method below
            """
            self.project = Project.objects.get(pk=pk)
            super(ProjectTrainingForm, self).__init__(*args, **kwargs)

        class Meta:
            model = Training
            exclude = ('project',)

        def save(self, commit=True):
            """
            Adds the project of the uploaded file through the <pk>
            we got during the initialization of the form
            """
            obj = super(ProjectTrainingForm, self).save(commit=False)

            # When we create the project we ask the user to submit a training file
            # but he should be able to skip this step and create the project without uploading
            # anything. It would be confusing to have a skip/upload button during the creation of the project
            # so we actually have 1 button called "Create" that submits the form. Since the .CSV training file
            # isn't mandatory, we cant have "required" in the file field, but we dont want to save an entry without
            # an uploaded file. Here we check if something was actually uploaded. If not we dont save and just return

            if obj.file:
                obj.project = self.project
                obj.save()
            return obj


