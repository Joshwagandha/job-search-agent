"""
Wellfound (formerly AngelList Talent) Jobs Scraper
Scrapes startup jobs from Wellfound
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging


logger = logging.getLogger(__name__)


def scrape_wellfound_jobs(roles: List[str] = None, max_results: int = 50) -> List[Dict]:
    """
    Scrape remote startup jobs from Wellfound
    
    Args:
        roles: List of role types to search for
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    if roles is None:
        roles = ['operations', 'customer-success', 'product-manager']
    
    jobs = []
    base_url = "https://wellfound.com/role"
    
    logger.info(f"Scraping Wellfound jobs for roles: {roles}")
    
    for role in roles:
        try:
            # Wellfound has role-specific pages
            url = f"{base_url}/{role}/remote"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse job listings
            job_cards = soup.find_all('div', {'data-test': 'JobSearchResult'})
            
            for card in job_cards[:15]:  # Limit per role
                try:
                    # Wellfound uses specific data attributes
                    title_elem = card.find('h2') or card.find('a', {'data-test': 'job-title'})
                    company_elem = card.find('div', {'data-test': 'company-name'})
                    location_elem = card.find('span', string=lambda x: x and 'Remote' in x)
                    link_elem = card.find('a', href=True)
                    
                    if title_elem:
                        job_url = link_elem['href'] if link_elem else url
                        if not job_url.startswith('http'):
                            job_url = f"https://wellfound.com{job_url}"
                        
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                            'location': 'Remote',
                            'description': '',
                            'url': job_url,
                            'source': 'Wellfound'
                        }
                        jobs.append(job)
                        
                        if len(jobs) >= max_results:
                            break
                            
                except Exception as e:
                    logger.warning(f"Error parsing Wellfound job card: {e}")
                    continue
            
            # Rate limiting
            time.sleep(3)
            
            if len(jobs) >= max_results:
                break
                
        except Exception as e:
            logger.error(f"Error scraping Wellfound for role '{role}': {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from Wellfound")
    return jobs
