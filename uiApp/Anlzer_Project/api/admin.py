from django.contrib import admin
from .models import Results, Query_languages, Query_properties, Query, Category_value, Category


class ResultsAdmin(admin.ModelAdmin):
    pass

class Query_languagesAdmin(admin.ModelAdmin):
    pass


class Query_propertiesAdmin(admin.ModelAdmin):
    pass


class QueryAdmin(admin.ModelAdmin):
    pass


class Category_valueAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Results, ResultsAdmin)
admin.site.register(Query_languages, Query_languagesAdmin)
admin.site.register(Query_properties, Query_propertiesAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Category_value, Category_valueAdmin)
admin.site.register(Category, CategoryAdmin)