from django.contrib import admin
from .models import Question, Answer, QuizResult

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')
    list_filter = ('question_type',)
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')
    list_filter = ('is_correct',)
    search_fields = ('text',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'visual_score', 'auditory_score', 'kinesthetic_score')
    search_fields = ('user',)
