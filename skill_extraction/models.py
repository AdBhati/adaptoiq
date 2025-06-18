from django.db import models

from assessment.models import JobRole, Skill
from authentication.models import TimeAudit, User

class CandidateSkillExtraction(TimeAudit):
    SOURCE_CHOICES = [
        ('Resume', 'Resume'),
        ('LinkedIn', 'LinkedIn'),
        ('Manual', 'Manual'),
    ]

    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skill_extractions")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    resume_file = models.FileField(upload_to="resumes/", null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.candidate.username} - {self.source} - {self.extracted_at}"
    
    class Meta:
        db_table = "candidate_skill_extractions"


class CandidateSkill(TimeAudit):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    extraction = models.ForeignKey(CandidateSkillExtraction, on_delete=models.CASCADE, related_name="skills", null=True, blank=True)
    proficiency_level = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ])
    
    def __str__(self):
        return f"{self.candidate.username} - {self.skill.name} ({self.proficiency_level})"

    class Meta:
        db_table = "candidate_skills"


class CandidateJobMatch(TimeAudit):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_matches")
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name="candidate_matches")
    match_percentage = models.FloatField()
    

    def __str__(self):
        return f"{self.candidate.username} - {self.job_role.title} - {self.match_percentage}%"

    class Meta:
        db_table = "candidate_job_matches"


