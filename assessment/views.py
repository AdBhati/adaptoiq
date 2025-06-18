from rest_framework import viewsets
from .models import User, JobRole, Skill, Question, CandidateAttempt, Assessment, AssessmentQuestion
from .serializers import (
    UserSerializer, JobRoleSerializer, SkillSerializer, QuestionSerializer,
    CandidateAttemptSerializer, AssessmentSerializer, AssessmentQuestionSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class JobRoleViewSet(viewsets.ModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class CandidateAttemptViewSet(viewsets.ModelViewSet):
    queryset = CandidateAttempt.objects.all()
    serializer_class = CandidateAttemptSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssessmentQuestion.objects.all()
    serializer_class = AssessmentQuestionSerializer
