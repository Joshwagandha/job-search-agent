"""
Y Combinator Jobs Scraper
Scrapes jobs from YC company job boards
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging


logger = logging.getLogger(__name__)


def scrape_yc_jobs(keywords: List[str] = None, max_pages: int = 3) -> List[Dict]:
    """
    Scrape jobs from Y Combinator Work at a Startup
    
    Args:
        keywords: List of keywords to search for
        max_pages: Maximum number of pages to scrape
    
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = ["customer", "operations", "support", "experience", "implementation"]
    
    jobs = []
    base_url = "https://www.workatastartup.com/jobs"
    
    logger.info(f"Scraping YC jobs with keywords: {keywords}")
    
    for keyword in keywords:
        try:
            # Build search URL
            params = {
                'query': keyword,
                'remote': 'true'  # Only remote jobs
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse job listings
            # Note: This is a placeholder structure - actual scraping would need
            # to match the real YC jobs page HTML structure
            job_cards = soup.find_all('div', class_='job-listing')
            
            for card in job_cards[:20]:  # Limit per keyword
                try:
                    job = {
                        'title': card.find('h2').text.strip() if card.find('h2') else 'Unknown',
                        'company': card.find('span', class_='company').text.strip() if card.find('span', class_='company') else 'Unknown',
                        'location': card.find('span', class_='location').text.strip() if card.find('span', class_='location') else 'Remote',
                        'description': card.find('p').text.strip() if card.find('p') else '',
                        'url': card.find('a')['href'] if card.find('a') else '',
                        'source': 'YC Work at a Startup'
                    }
                    jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
            # Be respectful - rate limit
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error scraping YC jobs for keyword '{keyword}': {e}")
            continue
    
    logger.info(f"Found {len(jobs)} jobs from YC")
    return jobs


def scrape_specific_yc_company(company_url: str) -> List[Dict]:
    """
    Scrape jobs from a specific YC company's careers page
    
    Args:
        company_url: URL to the company's careers page
    
    Returns:
        List of job dictionaries
    """
    jobs = []
    
    try:
        response = requests.get(company_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Generic job listing parsing
        # This would need to be customized per company
        job_links = soup.find_all('a', href=True)
        
        for link in job_links:
            if any(keyword in link.text.lower() for keyword in ['job', 'career', 'position', 'role']):
                job = {
                    'title': link.text.strip(),
                    'company': company_url.split('/')[2],
                    'location': 'Remote',  # Default
                    'description': '',
                    'url': link['href'] if link['href'].startswith('http') else f"{company_url}{link['href']}",
                    'source': company_url
                }
                jobs.append(job)
        
    except Exception as e:
        logger.error(f"Error scraping {company_url}: {e}")
    
    return jobs
