"""
Remote OK Job Board Scraper
Scrapes remote jobs from RemoteOK
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging


logger = logging.getLogger(__name__)


def scrape_remote_ok_jobs(keywords: List[str] = None, max_results: int = 40) -> List[Dict]:
    """
    Scrape remote jobs from Remote OK
    
    Args:
        keywords: List of keywords to search for
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = ['operations', 'customer', 'product']
    
    jobs = []
    base_url = "https://remoteok.com/remote-jobs"
    
    logger.info(f"Scraping Remote OK for keywords: {keywords}")
    
    for keyword in keywords:
        try:
            url = f"{base_url}/{keyword}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remote OK uses table rows for jobs
            job_rows = soup.find_all('tr', class_='job')
            
            for row in job_rows[:15]:  # Limit per keyword
                try:
                    # Remote OK has specific structure
                    title_elem = row.find('h2', itemprop='title')
                    company_elem = row.find('h3', itemprop='name')
                    link_elem = row.find('a', itemprop='url')
                    location_elem = row.find('div', class_='location')
                    
                    if title_elem and company_elem:
                        job_url = link_elem['href'] if link_elem else url
                        if not job_url.startswith('http'):
                            job_url = f"https://remoteok.com{job_url}"
                        
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                            'description': '',
                            'url': job_url,
                            'source': 'Remote OK'
                        }
                        jobs.append(job)
                        
                        if len(jobs) >= max_results:
                            break
                            
                except Exception as e:
                    logger.warning(f"Error parsing Remote OK job row: {e}")
                    continue
            
            # Rate limiting
            time.sleep(3)
            
            if len(jobs) >= max_results:
                break
                
        except Exception as e:
            logger.error(f"Error scraping Remote OK for keyword '{keyword}': {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from Remote OK")
    return jobs
