from django.db import models
import hashlib
from authentication.models import TimeAudit, User

class JobRole(TimeAudit):
    name = models.CharField(max_length=255, unique=True)
    required_skills = models.ManyToManyField('Skill', related_name="job_roles")
    required_proficiency = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "job_roles"


class Skill(TimeAudit):

    TECHNICAL = 'Technical'
    CORE = 'Core'
    SKILL_TYPE_CHOICES = [
        (TECHNICAL, 'Technical'),
        (CORE, 'Core'),
    ]

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=SKILL_TYPE_CHOICES, default=TECHNICAL)

    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "skills"


class Question(TimeAudit):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(unique=True)  # Ensure no exact duplicates
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_mcq = models.BooleanField(default=True)  # MCQ or Open-ended
    hash_value = models.CharField(max_length=64, unique=True, editable=False)  # For duplicate detection

    def save(self, *args, **kwargs):
        # Generate hash for duplicate detection
        self.hash_value = hashlib.sha256(self.text.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.skill.name} - {self.difficulty}"

    class Meta:
        db_table = "question_bank"


class CandidateAttempt(TimeAudit):
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'Candidate'}, related_name="attempts"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempts")
    answer_text = models.TextField(null=True, blank=True)  # For Open-ended
    is_correct = models.BooleanField(null=True)  # AI will update this
    difficulty_after = models.CharField(max_length=20, choices=Question.DIFFICULTY_CHOICES)

    def __str__(self):
        return f"Attempt by {self.candidate.username} - {self.question.text[:30]}"

    class Meta:
        db_table = "candidate_attempts"
        unique_together = ('candidate', 'question')  # Prevent duplicate attempts


class Assessment(TimeAudit):
    hr = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'HR'}, related_name="assessments_created"
    )
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'Candidate'}, related_name="assessments_taken"
    )
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name="assessments")

    def __str__(self):
        return f"{self.candidate.username} - {self.job_role.name}"

    class Meta:
        db_table = "assessments"


class AssessmentQuestion(TimeAudit):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="assessment_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="assessment_questions")

    def __str__(self):
        return f"{self.assessment.candidate.username} - {self.question.text[:30]}"

    class Meta:
        db_table = "assessment_questions"
        unique_together = ('assessment', 'question')  # Prevent duplicate questions


class QuestionDuplicate(TimeAudit):
    hash_value = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"Duplicate Hash: {self.hash_value}"

    class Meta:
        db_table = "question_duplicates"



