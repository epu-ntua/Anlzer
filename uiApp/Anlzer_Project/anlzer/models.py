from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models.signals import post_save


class Provider(models.Model):
    """
    The class for providers. Adding a new one is as easy as adding an object here
    As on 04/2016 the current providers are: Facebook, Twitter, Instagram
    """
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' % self.name.capitalize()


class TimeStampedModel(models.Model):
    """
    All classed will inherit from this class to denote when they were created
    This class can easily be extended by adding an "updated_on" field as well
    """
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserExtraData(TimeStampedModel):
    USER_TYPES = (
        ('COMPANY', 'Company'),
        ('INDIVIDUAL', 'Individual'),
    )

    user = models.OneToOneField(User, related_name='extra_data')
    user_type = models.CharField(default='COMPANY', choices=USER_TYPES, max_length=50)
    under_company = models.ForeignKey(User, default=None, null=True, blank=True)

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        if created:
            UserExtraData(user=instance).save()

# creates a UserExtraData instance after a User is created
post_save.connect(UserExtraData.post_save, sender=User)


class AnlzerContentModel(TimeStampedModel):
    """
    An abstract class that stores common info used between the basic
    classes of the Anlzer platform
    """
    user = models.ForeignKey(User, related_name='%(class)ss', null=True)
    title = models.CharField(max_length=58)
    pages = models.CharField(max_length=1000)
    hashtags = models.CharField(max_length=1000)
    provider = models.ManyToManyField(Provider)

    slug = models.SlugField(max_length=100, null=True)

    def provider_to_string(self):
        return ','.join(p.name for p in self.provider.all())

    class Meta:
        abstract = True


class Project(AnlzerContentModel):
    """
    The basic class for an Anlzer Project.
    """
    description = models.CharField(max_length=110, blank=True, null=True, default=None)
    product = models.CharField(max_length=200, null=True)
    service = models.CharField(max_length=200, null=True)


    def __unicode__(self):
        return 'Project <%s> that was created on %s' % (
            self.title.title(),
            self.created_on
        )

    # Unique title per user
    class Meta:
        unique_together = (
            ("user", "title"),
        )


class Report(AnlzerContentModel):
    """
    The basic class for a Report of a project.
    The reports are either live or not.

    When they are live then live field is True and the live_date_range field
    has the days from today to perform the analysis (i.e. last 30 days = 30)

    When they are not live then the live field is falase, the live_date_range
    is none and the start_date and end_date fields contain the date boundaries
    of the analysis
    """
    LIVE_CHOICES = (
        ('LAST_DAY', 'Previous Day'),
        ('LAST_WEEK', 'Last 7 Days'),
        ('LAST_MONTH', 'Last 30 Days'),
        ('LAST_YEAR', 'Last Year'),
    )

    # If it's live it's always gonna be recurring when not running. Else its either running or completed
    STATUS_CHOICES = (
        ('RECURRING', 'Recurring'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed')
    )
    project = models.ForeignKey(Project, related_name='reports')
    live = models.BooleanField(default=True)
    live_range = models.CharField(max_length=100, choices=LIVE_CHOICES, null=True, default=None)
    start_date = models.DateField(null=True, default=None, blank=True)
    end_date = models.DateField(null=True, default=None, blank=True)
    status = models.CharField(default="RECURRING", choices=STATUS_CHOICES, max_length=50)

    def shares_exact_project_sources(self):
        same_hashtags = self.hashtags == self.project.hashtags
        same_pages = self.pages == self.project.pages
        same_provider = self.provider_to_string() == self.project.provider_to_string()

        return same_hashtags and same_pages and same_provider

    def shares_some_project_sources(self):
        report_pages_list = self.pages.split(',')
        report_hashtag_list = self.hashtags.split(',')

        project_pages_list = self.project.pages.split(',')
        project_hashtag_list = self.project.pages.split(',')

        share_some_common_pages = not set(report_pages_list).isdisjoint(project_pages_list)
        share_some_common_hashtags = not set(report_hashtag_list).isdisjoint(project_hashtag_list)

        return share_some_common_hashtags and share_some_common_pages

    def get_sources_choice(self):
        if self.shares_exact_project_sources():
            return 'USE_PROJECT_SOURCES'

        elif self.shares_some_project_sources():
            return 'MODIFY_PROJECT_SOURCES'
        else:
            return 'DEFINE_CUSTOM_SOURCES'

    def get_live_interval(self):
        interval_dict = {
            'LAST_DAY': 1,
            'LAST_WEEK': 7,
            'LAST_MONTH': 30,
            'LAST_YEAR': 365
        }

        if not self.live:
            return None
        return interval_dict[self.live_range]

    def get_run_status(self):
        if not self.live:
            if self.status == "COMPLETED":
                return "Completed"
            elif self.status == "RUNNING":
                return "Running"
        else:
            return 'Running daily at: %s' % (
                self.created_on.strftime('%H:%M')
            )

    # unique report-project-user combination
    class Meta:
        unique_together = (
            ("project", "title"),
        )


def upload_path_handler(instance, filename):
    """
    A function for determining the upload directory of each training
    Unfortunately this is not a method so it cannot be declared inside of a
    class
    """
    return "trainings/%s/%s/" % (instance.project.title, filename)


class Training(TimeStampedModel):
    """
    The model for the training files that are uploaded
    for each project on Anlzer
    """
    project = models.ForeignKey(Project, related_name='training')
    file = models.FileField(upload_to=upload_path_handler, blank=True, null=True, default=None)

    def __unicode__(self):
        return '<%s> for project <%s>' % (
            self.file,
            self.project.title
        )


class Comment(TimeStampedModel):
    author = models.ForeignKey(User, related_name='comments')
    project = models.ForeignKey(Project, related_name='comments')
    message = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return '<%s> said: <%s>' % (
            self.author.username,
            self.message
        )
# ----------------------------------------------------------------------------------------------------------------------

def get_company_accounts(self):
    """
    A method that takes a Company User and returns the invididual accounts under this company
    """
    return [u.user for u in UserExtraData.objects.filter(under_company=self)]


def is_company(self):
    """
    Returns True if the currently logged in user is a company
    """
    return UserExtraData.objects.get(user=self).user_type == 'COMPANY'

User.add_to_class("get_company_accounts", get_company_accounts)
User.add_to_class("is_company", is_company)

