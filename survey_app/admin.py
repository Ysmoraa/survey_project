from django.contrib import admin
from .models import Survey, Question, Option, Response, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    inlines = [OptionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    readonly_fields = ('question', 'text_answer', 'option_answer', 'rating_answer')
    extra = 0

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'is_published')
        }),
        ('Información avanzada', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'respondent', 'created_at')
    list_filter = ('survey', 'created_at')
    inlines = [AnswerInline]
    readonly_fields = ('created_at',)