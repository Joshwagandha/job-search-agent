"""
Job Scoring Module
Analyzes job postings and scores them based on fit criteria
"""

import json
from pathlib import Path
from typing import Dict, List


class JobScorer:
    def __init__(self, config_path: str = "config.json"):
        """Initialize scorer with configuration"""
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.criteria = config['job_search_criteria']
        self.weights = config['scoring_weights']
    
    def score_job(self, job: Dict) -> Dict:
        """
        Score a job posting based on criteria
        
        Args:
            job: Dictionary containing job details
                {
                    'title': str,
                    'company': str,
                    'location': str,
                    'description': str,
                    'url': str,
                    'source': str
                }
        
        Returns:
            Dictionary with scores and reasoning
        """
        scores = {
            'remote_score': self._score_remote(job),
            'industry_score': self._score_industry(job),
            'role_score': self._score_role(job),
            'company_stage_score': self._score_company_stage(job),
            'skills_score': self._score_skills(job)
        }
        
        # Calculate weighted total
        total_score = sum(
            scores[key.replace('_score', '') + '_score'] * self.weights[key.replace('_score', '') + '_match']
            for key in scores.keys()
        )
        
        # Check for deal-breakers
        deal_breakers = self._check_deal_breakers(job)
        
        return {
            'job': job,
            'total_score': round(total_score, 2),
            'scores': scores,
            'deal_breakers': deal_breakers,
            'passed': total_score >= 0.5 and not deal_breakers
        }
    
    def _score_remote(self, job: Dict) -> float:
        """Score based on remote work requirement"""
        location = job.get('location', '').lower()
        description = job.get('description', '').lower()
        
        # Deal-breaker: must be remote
        if any(phrase in location or phrase in description for phrase in [
            'on-site', 'onsite', 'in-office', 'office-based', 'hybrid'
        ]):
            return 0.0
        
        if any(phrase in location or phrase in description for phrase in [
            'remote', 'work from home', 'wfh', 'distributed', 'anywhere'
        ]):
            return 1.0
        
        return 0.3  # Unknown, but possible
    
    def _score_industry(self, job: Dict) -> float:
        """Score based on industry match"""
        company = job.get('company', '').lower()
        description = job.get('description', '').lower()
        combined = f"{company} {description}"
        
        matches = 0
        for industry in self.criteria['target_industries']:
            if industry.lower() in combined:
                matches += 1
        
        # Normalize to 0-1 scale
        return min(matches / 3, 1.0)  # Cap at 3 industry matches
    
    def _score_role(self, job: Dict) -> float:
        """Score based on role/title match"""
        title = job.get('title', '').lower()
        
        for target_role in self.criteria['target_roles']:
            # Check if key words from target role are in job title
            role_words = set(target_role.lower().split())
            title_words = set(title.split())
            
            # Calculate word overlap
            overlap = len(role_words & title_words) / len(role_words)
            if overlap >= 0.5:  # At least 50% word match
                return overlap
        
        return 0.0
    
    def _score_company_stage(self, job: Dict) -> float:
        """Score based on company stage preference"""
        company = job.get('company', '').lower()
        description = job.get('description', '').lower()
        combined = f"{company} {description}"
        
        for stage in self.criteria['company_stage']:
            if stage.lower() in combined:
                return 1.0
        
        # Check for startup indicators
        startup_indicators = ['startup', 'early stage', 'growing team', 'series a', 'series b', 'yc', 'y combinator']
        if any(indicator in combined for indicator in startup_indicators):
            return 0.8
        
        return 0.3  # Unknown
    
    def _score_skills(self, job: Dict) -> float:
        """Score based on required skills match"""
        description = job.get('description', '').lower()
        
        matches = 0
        for skill in self.criteria['required_skills']:
            if skill.lower() in description:
                matches += 1
        
        # Normalize to 0-1 scale
        return min(matches / 5, 1.0)  # Cap at 5 skill matches
    
    def _check_deal_breakers(self, job: Dict) -> List[str]:
        """Check for deal-breaker requirements"""
        deal_breakers = []
        location = job.get('location', '').lower()
        description = job.get('description', '').lower()
        combined = f"{location} {description}"
        
        # Check location deal-breakers
        if any(phrase in combined for phrase in ['hybrid', 'in-office', 'on-site', 'relocation required']):
            deal_breakers.append("Not fully remote")
        
        # Check avoided requirements
        for avoid_req in self.criteria['avoid']['requirements']:
            if avoid_req.lower() in combined:
                deal_breakers.append(f"Contains: {avoid_req}")
        
        return deal_breakers


def score_jobs_batch(jobs: List[Dict], config_path: str = "config.json") -> List[Dict]:
    """
    Score a batch of jobs and return sorted by score
    
    Args:
        jobs: List of job dictionaries
        config_path: Path to config file
    
    Returns:
        List of scored jobs, sorted by total_score descending
    """
    scorer = JobScorer(config_path)
    scored_jobs = [scorer.score_job(job) for job in jobs]
    
    # Filter passed jobs and sort by score
    passed_jobs = [j for j in scored_jobs if j['passed']]
    passed_jobs.sort(key=lambda x: x['total_score'], reverse=True)
    
    return passed_jobs
