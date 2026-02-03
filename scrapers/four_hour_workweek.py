"""
4-Hour Workweek Job Board Scraper
Scrapes remote jobs from Tim Ferriss's job board
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging


logger = logging.getLogger(__name__)


def scrape_4hw_jobs(max_results: int = 30) -> List[Dict]:
    """
    Scrape remote jobs from 4-Hour Workweek job board
    
    Args:
        max_results: Maximum number of jobs to return
    
    Returns:
        List of job dictionaries
    """
    jobs = []
    # The 4HWW job board is typically hosted on external platforms
    # Common URLs include job boards they partner with
    urls = [
        "https://www.fourhourworkweek.com/blog/jobs/",
        "https://jobs.workable.com/fourhourworkweek"
    ]
    
    logger.info("Scraping 4-Hour Workweek job board")
    
    for url in urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic job listing parsing
            # Look for common job board patterns
            job_links = soup.find_all('a', href=True, string=lambda x: x and any(
                keyword in x.lower() for keyword in 
                ['manager', 'operations', 'customer', 'product', 'remote']
            ))
            
            for link in job_links[:max_results]:
                try:
                    job_url = link['href']
                    if not job_url.startswith('http'):
                        job_url = f"{url.rstrip('/')}/{job_url.lstrip('/')}"
                    
                    job = {
                        'title': link.get_text(strip=True),
                        'company': '4HWW Partner',
                        'location': 'Remote',
                        'description': '',
                        'url': job_url,
                        'source': '4-Hour Workweek'
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    logger.warning(f"Error parsing 4HWW job link: {e}")
                    continue
            
            if jobs:  # If we found jobs on this URL, no need to check others
                break
            
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error scraping 4HWW job board at {url}: {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from 4-Hour Workweek")
    return jobs
