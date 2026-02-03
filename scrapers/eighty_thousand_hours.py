"""
80,000 Hours Job Board Scraper
Scrapes impact-focused jobs from 80,000 Hours
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging


logger = logging.getLogger(__name__)


def scrape_80k_hours_jobs(max_results: int = 30) -> List[Dict]:
    """
    Scrape jobs from 80,000 Hours job board
    
    Args:
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    jobs = []
    base_url = "https://80000hours.org/job-board/"
    
    logger.info("Scraping 80,000 Hours job board")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 80k Hours uses a specific job board structure
        job_listings = soup.find_all('article', class_='job-board__job')
        
        if not job_listings:
            # Fallback: look for any article or div with job-related classes
            job_listings = soup.find_all(['article', 'div'], class_=lambda x: x and 'job' in x.lower())
        
        for listing in job_listings[:max_results]:
            try:
                # Try to find title
                title_elem = (
                    listing.find('h2') or 
                    listing.find('h3') or
                    listing.find('a', class_=lambda x: x and 'title' in x.lower())
                )
                
                # Try to find company/organization
                company_elem = (
                    listing.find('div', class_=lambda x: x and 'org' in x.lower()) or
                    listing.find('span', class_=lambda x: x and 'company' in x.lower())
                )
                
                # Try to find link
                link_elem = listing.find('a', href=True)
                
                # Look for remote indicator
                location_text = listing.get_text()
                is_remote = any(keyword in location_text.lower() for keyword in ['remote', 'anywhere', 'location flexible'])
                
                if title_elem:
                    job_url = link_elem['href'] if link_elem else base_url
                    if not job_url.startswith('http'):
                        job_url = f"https://80000hours.org{job_url}"
                    
                    # Only include if remote or location not specified
                    job = {
                        'title': title_elem.get_text(strip=True),
                        'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                        'location': 'Remote' if is_remote else 'See job posting',
                        'description': '',
                        'url': job_url,
                        'source': '80,000 Hours'
                    }
                    jobs.append(job)
                    
            except Exception as e:
                logger.warning(f"Error parsing 80k Hours job listing: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error scraping 80,000 Hours job board: {e}")
    
    logger.info(f"Found {len(jobs)} jobs from 80,000 Hours")
    return jobs
