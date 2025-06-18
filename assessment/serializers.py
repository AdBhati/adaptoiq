from rest_framework import serializers
from .models import User, JobRole, Skill, Question, CandidateAttempt, Assessment, AssessmentQuestion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CandidateAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateAttempt
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = '__all__'
