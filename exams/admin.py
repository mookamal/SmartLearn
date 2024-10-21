from django.contrib import admin
from . import models
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'subject', 'is_approved',
                    'created_at', 'approval_date')

    list_filter = ('is_approved', 'exam', 'subject', 'created_at')

    search_fields = ('text', 'explanation', 'exam__name', 'subject__name')

    readonly_fields = ('created_at', 'approval_date')

    class ChoiceInline(admin.TabularInline):
        model = models.Choice
        extra = 1

    inlines = [ChoiceInline]


admin.site.register(models.Question, QuestionAdmin)


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


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


admin.site.register(models.Subject, SubjectAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent_source', 'created_at')
    search_fields = ('name', 'category__name')


admin.site.register(models.Source, SourceAdmin)
