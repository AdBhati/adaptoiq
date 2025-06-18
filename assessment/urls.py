from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, JobRoleViewSet, SkillViewSet, QuestionViewSet,
    CandidateAttemptViewSet, AssessmentViewSet, AssessmentQuestionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'job_roles', JobRoleViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'candidate_attempts', CandidateAttemptViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'assessment_questions', AssessmentQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
