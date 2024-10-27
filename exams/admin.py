from django.contrib import admin
from . import models
from import_export import fields, resources
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin


class QuestionResource(resources.ModelResource):
    choices = fields.Field(
        column_name='choices',
        attribute='choices',
        widget=ManyToManyWidget(models.Choice, separator=',', field='text')
    )

    class Meta:
        model = models.Question
        fields = ('id', 'text', 'exam__name', 'subject__name',
                  'is_approved', 'created_at', 'choices')


@admin.register(models.Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('text', 'exam', 'subject', 'is_approved',
                    'created_at', 'approval_date')
    list_filter = ('is_approved', 'exam', 'subject', 'created_at')
    search_fields = ('text', 'explanation', 'exam__name', 'subject__name')
    readonly_fields = ('created_at', 'approval_date')

    class ChoiceInline(admin.TabularInline):
        model = models.Choice
        extra = 1

    inlines = [ChoiceInline]


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_visible', 'created_at')
    list_filter = ('category', 'is_visible')
    search_fields = ('name', 'category__name')


admin.site.register(models.Exam, ExamAdmin)
admin.site.register(models.Answer)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'is_listed')
    list_filter = ('is_listed', 'parent_category')
    search_fields = ('name',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Session)
admin.site.register(models.Issue)
admin.site.register(models.Choice)
admin.site.register(models.TestCategory)
admin.site.register(models.TestRow)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


admin.site.register(models.Subject, SubjectAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent_source', 'created_at')
    search_fields = ('name', 'category__name')


admin.site.register(models.Source, SourceAdmin)
