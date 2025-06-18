from django.urls import path

from skill_extraction.views import MatchJobRoleViewSet, SkillExtractionViewSet



urlpatterns = [
    path("resume-extraction/", SkillExtractionViewSet.as_view({"post": "resume_extraction"})),
    path("linkdin-extraction/", SkillExtractionViewSet.as_view({"post": "linkedin_extraction"})),
    path("match-job-role/", MatchJobRoleViewSet.as_view({"post": "match_job_role"})),
]
