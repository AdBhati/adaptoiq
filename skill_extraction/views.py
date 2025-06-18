from django.shortcuts import render
import fitz  # PyMuPDF
import docx
import re
import requests
from bs4 import BeautifulSoup
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from assessment.models import Skill
from services.linkdin import PDLService
from services.open_ai import ResumeSkillExtractor

from services.skill_matching_service import SkillMatchingService
from skill_extraction.models import CandidateSkill, CandidateSkillExtraction
import textract
import os

from utils.helpers import api_response


def extract_text_from_pdf(file):
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise Exception(f"PDF reading failed: {str(e)}")

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise Exception(f"DOCX reading failed: {str(e)}")
        
    
def extract_text_from_file(file):
    extension = os.path.splitext(file.name)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file)
    elif extension in [".docx"]:
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format")


class SkillExtractionViewSet(viewsets.ViewSet):
    """ViewSet for skill extraction from Resume"""
    
    permission_classes = [IsAuthenticated]

    
    def resume_extraction(self, request):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({"error": "No resume file uploaded"}, status=400)

        try:
            text = extract_text_from_file(resume_file)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        try:
            extractor = ResumeSkillExtractor()
            ai_response = extractor.extract_info_from_resume(text)

            
            # print("Raw AI Response:", ai_response, type(ai_response))

        
            if not isinstance(ai_response, dict):
                return Response(api_response(
                    False,
                    "AI response is not a valid dictionary",
                    {"raw_response": ai_response},
                    500
                ), status=500)

            
            if "error" in ai_response:
                return Response(api_response(
                    False,
                    ai_response["error"],
                    {"raw_response": ai_response.get("raw_response", "")},
                    500
                ), status=500)

            skills_data = ai_response.get("skills", [])
            extraction = CandidateSkillExtraction.objects.create(
                candidate=request.user,
                source="Resume",
                resume_file=resume_file
            )

            for skill_name in skills_data:
                if not isinstance(skill_name, str):
                    continue

                skill_name = skill_name.strip()
                # proficiency = skill_info.get("proficiency")

                if not skill_name:
                    print("skill_name")
                    continue

                skill_obj, _ = Skill.objects.get_or_create(
                    name__iexact=skill_name.strip(),
                    defaults={"name": skill_name.strip()}
                )

                CandidateSkill.objects.create(
                    candidate=request.user,
                    skill=skill_obj,
                    extraction=extraction,
                    # proficiency_level=proficiency
                )

            return Response(api_response(
                True,
                "Resume processed and skills stored successfully",
                ai_response,
                200
            ), status=200)

        except Exception as e:
            return Response(api_response(False, str(e), {}, 500), status=500)


    def linkedin_extraction(self, request):
        linkedin_url = request.data.get("linkedin_url")
        if not linkedin_url:
            return Response(api_response(False, "No LinkedIn URL provided", {}, 400), status=400)

        try:
            scraper = PDLService()
            profile_data = scraper.fetch_profile_data(linkedin_url)

            if "error" in profile_data:
                return Response(api_response(False, profile_data["error"], {}, 500), status=500)

            skills_data = profile_data.get("skills", [])
            extraction = CandidateSkillExtraction.objects.create(
                candidate=request.user,
                source="LinkedIn",
                linkedin_url=linkedin_url
            )

            for skill_info in skills_data:
                skill_name = skill_info.get("name")
                proficiency = skill_info.get("proficiency")

                if not skill_name or not proficiency:
                    continue

                skill_obj, _ = Skill.objects.get_or_create(
                    name__iexact=skill_name.strip(),
                    defaults={"name": skill_name.strip()}
                )

                CandidateSkill.objects.create(
                    candidate=request.user,
                    skill=skill_obj,
                    extraction=extraction,
                    proficiency_level=proficiency
                )

            return Response(api_response(True, "LinkedIn data processed successfully", profile_data, 200), status=200)

        except Exception as e:
            return Response(api_response(False, str(e), {}, 500), status=500)
        

class MatchJobRoleViewSet(viewsets.ViewSet):
    """ViewSet for matching candidate skills with job roles"""
    permission_classes = [IsAuthenticated]

    def match_job_role(self, request):
        """Match candidate skills with a job role"""
        candidate_id = request.data.get("candidate_id", request.user.id)
        job_role_id = request.data.get("job_role_id")
        
        if not job_role_id:
            return Response(api_response(
                False, "Job role ID is required", {}, 400
            ), status=400)
        
        try:
            matching_service = SkillMatchingService()
            match_result = matching_service.calculate_match_percentage(candidate_id, job_role_id)
            
            return Response(api_response(
                True, 
                "Match percentage calculated successfully", 
                match_result, 
                200
            ), status=200)
        
        except ValueError as e:
            return Response(api_response(
                False, str(e), {}, 404
            ), status=404)
        
        except Exception as e:
            return Response(api_response(
                False, str(e), {}, 500
            ), status=500)




            
        

        