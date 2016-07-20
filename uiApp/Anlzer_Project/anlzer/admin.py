from django.contrib import admin
from .models import *


class UserExtraDataAdmin(admin.ModelAdmin):
    pass

class ProviderAdmin(admin.ModelAdmin):
    fields = ('name',)


class ProjectAdmin(admin.ModelAdmin):
    pass


class TrainingAdmin(admin.ModelAdmin):
    pass


class ReportAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(UserExtraData, UserExtraDataAdmin)
admin.site.register(Comment, CommentAdmin)