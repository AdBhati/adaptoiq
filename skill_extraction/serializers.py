from rest_framework import serializers
from .models import CandidateJobMatch, CandidateSkill, CandidateSkillExtraction
from assessment.serializers import JobRoleSerializer, SkillSerializer
from assessment.models import JobRole, Skill

class CandidateJobMatchSerializer(serializers.ModelSerializer):
    job_role = JobRoleSerializer(read_only=True)
    
    class Meta:
        model = CandidateJobMatch
        fields = ['id', 'candidate', 'job_role', 'match_percentage', 'created_at']