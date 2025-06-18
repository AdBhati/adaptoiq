from assessment.models import JobRole, Skill
from authentication.models import User
from skill_extraction.models import CandidateSkill, CandidateJobMatch

class SkillMatchingService:
    """Service to calculate skill matches between candidates and job roles"""
    
    @staticmethod
    def calculate_match_percentage(candidate_id, job_role_id):
        """
        Calculate the match percentage between a candidate and job role
        
        Args:
            candidate_id: ID of the candidate user
            job_role_id: ID of the job role to match against
            
        Returns:
            dict with match percentage and details
        """
        try:
            # Get the candidate and job role
            candidate = User.objects.get(id=candidate_id, role='Candidate')
            job_role = JobRole.objects.get(id=job_role_id)
            
            # Get required skills for the job role
            required_skills = job_role.required_skills.all()
            required_skill_ids = set(required_skills.values_list('id', flat=True))
            total_required = len(required_skill_ids)
            
            if total_required == 0:
                return {
                    "match_percentage": 0,
                    "matched_skills": [],
                    "missing_skills": []
                }
            
            # Get candidate skills
            candidate_skills = CandidateSkill.objects.filter(candidate=candidate)
            candidate_skill_map = {skill.skill_id: skill for skill in candidate_skills}
            candidate_skill_ids = set(candidate_skill_map.keys())
            
            # Calculate matches
            matched_skill_ids = required_skill_ids.intersection(candidate_skill_ids)
            missing_skill_ids = required_skill_ids - candidate_skill_ids
            
            # Calculate match percentage - simple version without proficiency bonuses
            match_percentage = (len(matched_skill_ids) / total_required) * 100
            
            # Get detailed match information
            matched_skills = []
            for skill_id in matched_skill_ids:
                candidate_skill = candidate_skill_map[skill_id]
                skill = candidate_skill.skill
                
                matched_skills.append({
                    "id": skill.id,
                    "name": skill.name,
                    "type": skill.type,
                    "proficiency": candidate_skill.proficiency_level
                })
            
            # Get missing skills
            missing_skills = []
            for skill_id in missing_skill_ids:
                skill = Skill.objects.get(id=skill_id)
                missing_skills.append({
                    "id": skill.id,
                    "name": skill.name,
                    "type": skill.type,
                })
            
            # Store the match result
            match_result = CandidateJobMatch.objects.create(
                candidate=candidate,
                job_role=job_role,
                match_percentage=round(match_percentage, 2)
            )
            
            return {
                "match_percentage": round(match_percentage, 2),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "match_id": match_result.id
            }
            
        except User.DoesNotExist:
            raise ValueError(f"Candidate with ID {candidate_id} not found")
        except JobRole.DoesNotExist:
            raise ValueError(f"Job Role with ID {job_role_id} not found")
        except Exception as e:
            raise Exception(f"Error calculating match: {str(e)}")