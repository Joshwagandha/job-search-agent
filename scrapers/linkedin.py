"""
LinkedIn Jobs Scraper
Scrapes remote jobs from LinkedIn
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging
from urllib.parse import urlencode


logger = logging.getLogger(__name__)


def scrape_linkedin_jobs(keywords: List[str] = None, max_results: int = 50) -> List[Dict]:
    """
    Scrape remote jobs from LinkedIn
    
    Args:
        keywords: List of job title keywords
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = [
            "Customer Operations Manager",
            "Customer Experience Manager",
            "Operations Manager",
            "Product Manager Operations",
            "Implementation Manager"
        ]
    
    jobs = []
    base_url = "https://www.linkedin.com/jobs/search"
    
    logger.info(f"Scraping LinkedIn jobs for keywords: {keywords}")
    
    for keyword in keywords:
        try:
            # Build search parameters
            params = {
                'keywords': keyword,
                'location': 'United States',
                'f_WT': '2',  # Remote filter
                'f_TPR': 'r86400',  # Posted in last 24 hours
                'position': 1,
                'pageNum': 0
            }
            
            url = f"{base_url}?{urlencode(params)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse job cards
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards[:10]:  # Limit per keyword
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else 'Remote',
                            'description': '',  # Would need to fetch individual job page
                            'url': link_elem['href'] if link_elem else url,
                            'source': 'LinkedIn'
                        }
                        jobs.append(job)
                        
                        if len(jobs) >= max_results:
                            break
                            
                except Exception as e:
                    logger.warning(f"Error parsing LinkedIn job card: {e}")
                    continue
            
            # Rate limiting
            time.sleep(3)
            
            if len(jobs) >= max_results:
                break
                
        except Exception as e:
            logger.error(f"Error scraping LinkedIn for keyword '{keyword}': {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from LinkedIn")
    return jobs
