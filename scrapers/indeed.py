"""
Indeed Jobs Scraper
Scrapes remote jobs from Indeed
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging
from urllib.parse import urlencode


logger = logging.getLogger(__name__)


def scrape_indeed_jobs(keywords: List[str] = None, max_results: int = 50) -> List[Dict]:
    """
    Scrape remote jobs from Indeed
    
    Args:
        keywords: List of job title keywords
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = [
            "Internal Tools"
            "Product Manager"
            "Customer Operations Manager remote",
            "Customer Experience Manager remote",
            "Operations Manager remote",
            "Implementation Manager remote"
        ]
    
    jobs = []
    base_url = "https://www.indeed.com/jobs"
    
    logger.info(f"Scraping Indeed jobs for keywords: {keywords}")
    
    for keyword in keywords:
        try:
            # Build search parameters
            params = {
                'q': keyword,
                'l': 'Remote',
                'fromage': '1',  # Last 24 hours
                'sort': 'date'
            }
            
            url = f"{base_url}?{urlencode(params)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse job cards (Indeed uses different selectors)
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:10]:  # Limit per keyword
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    
                    if title_elem and company_elem:
                        job_id = link_elem.get('data-jk', '') if link_elem else ''
                        job_url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else url
                        
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                            'description': '',
                            'url': job_url,
                            'source': 'Indeed'
                        }
                        jobs.append(job)
                        
                        if len(jobs) >= max_results:
                            break
                            
                except Exception as e:
                    logger.warning(f"Error parsing Indeed job card: {e}")
                    continue
            
            # Rate limiting
            time.sleep(3)
            
            if len(jobs) >= max_results:
                break
                
        except Exception as e:
            logger.error(f"Error scraping Indeed for keyword '{keyword}': {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from Indeed")
    return jobs
