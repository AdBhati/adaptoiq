from django.contrib import admin
from .models import User, JobRole, Skill, Question, CandidateAttempt, Assessment, AssessmentQuestion, QuestionDuplicate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill', 'difficulty', 'is_mcq')
    search_fields = ('text',)
    list_filter = ('difficulty', 'skill')

@admin.register(CandidateAttempt)
class CandidateAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'question', 'is_correct', 'difficulty_after')
    list_filter = ('is_correct', 'difficulty_after')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'hr', 'candidate', 'job_role', 'created_at')
    list_filter = ('job_role',)

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment', 'question')

@admin.register(QuestionDuplicate)
class QuestionDuplicateAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash_value')
    search_fields = ('hash_value',)
