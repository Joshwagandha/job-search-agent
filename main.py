#!/usr/bin/env python3
"""
Job Search Automation Agent
Runs daily scraping, analysis, and summary generation
"""

import argparse
import json
import logging
import os
from datetime import datetime
from pathlib import Path

# Import scrapers and analyzers
from scrapers.yc_jobs import scrape_yc_jobs
from scrapers.linkedin import scrape_linkedin_jobs
from scrapers.indeed import scrape_indeed_jobs
from scrapers.wellfound import scrape_wellfound_jobs
from scrapers.four_hour_workweek import scrape_4hw_jobs
from scrapers.eighty_thousand_hours import scrape_80k_hours_jobs
from scrapers.remote_ok import scrape_remote_ok_jobs
from analyzers.scorer import score_jobs_batch

# Create logs directory before setting up logging
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)


def generate_summary(scored_jobs: list, date: str) -> str:
    """
    Generate a markdown summary of job search results
    
    Args:
        scored_jobs: List of scored job dictionaries
        date: Date string (YYYY-MM-DD)
    
    Returns:
        Markdown formatted summary
    """
    summary = f"""# Job Search Summary - {date}

## 🎯 Overview

Found **{len(scored_jobs)}** matching jobs today!

"""
    
    if not scored_jobs:
        summary += """No jobs found matching your criteria today. The search continues tomorrow!

### Next Steps
- Scrapers will run again tomorrow
- Check back for new opportunities
"""
        return summary
    
    # Top 10 jobs
    summary += "## 🌟 Top Opportunities\n\n"
    
    for i, job_result in enumerate(scored_jobs[:10], 1):
        job = job_result['job']
        score = job_result['total_score']
        scores = job_result['scores']
        
        summary += f"""### {i}. {job['title']} at {job['company']}

**Score:** {score}/1.0  
**Location:** {job['location']}  
**Source:** {job['source']}  
**URL:** {job['url']}

**Why it's a match:**
- Remote Match: {scores['remote_score']:.0%}
- Industry Match: {scores['industry_score']:.0%}
- Role Match: {scores['role_score']:.0%}
- Skills Match: {scores['skills_score']:.0%}

---

"""
    
    # Stats
    summary += f"""## 📊 Statistics

- Total jobs scraped: {len(scored_jobs)}
- Jobs meeting criteria: {len(scored_jobs)}
- Average score: {sum(j['total_score'] for j in scored_jobs) / len(scored_jobs):.2f}
- Top score: {max(j['total_score'] for j in scored_jobs):.2f}

## 🛠️ Sources

- LinkedIn
- Indeed
- Wellfound (AngelList)
- Y Combinator Work at a Startup
- 4-Hour Workweek Job Board
- 80,000 Hours
- Remote OK

---
*Generated automatically by Job Search Agent*
"""
    
    return summary

def main():
    parser = argparse.ArgumentParser(description='Job Search Automation Agent')
    parser.add_argument('--daily-summary', action='store_true', 
                       help='Run daily scraping and generate summary')
    parser.add_argument('--scrape-only', action='store_true',
                       help='Only scrape, no summary')
    parser.add_argument('--company', type=str,
                       help='Scrape specific company')
    
    args = parser.parse_args()
    
    logging.info("Starting Job Search Agent")
    
    if args.daily_summary:
        logging.info("Running daily summary workflow")
        
        # Create directories if they don't exist
        Path('summaries').mkdir(exist_ok=True)
        Path('data').mkdir(exist_ok=True)
        Path('logs').mkdir(exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Scrape jobs from all sources
        all_jobs = []
        
        logging.info("Scraping LinkedIn jobs...")
        try:
            linkedin_jobs = scrape_linkedin_jobs()
            all_jobs.extend(linkedin_jobs)
        except Exception as e:
            logger.error(f"LinkedIn scraper failed: {e}")
        
        logging.info("Scraping Indeed jobs...")
        try:
            indeed_jobs = scrape_indeed_jobs()
            all_jobs.extend(indeed_jobs)
        except Exception as e:
            logger.error(f"Indeed scraper failed: {e}")
        
        logging.info("Scraping Wellfound jobs...")
        try:
            wellfound_jobs = scrape_wellfound_jobs()
            all_jobs.extend(wellfound_jobs)
        except Exception as e:
            logger.error(f"Wellfound scraper failed: {e}")
        
        logging.info("Scraping YC jobs...")
        try:
            yc_jobs = scrape_yc_jobs()
            all_jobs.extend(yc_jobs)
        except Exception as e:
            logger.error(f"YC scraper failed: {e}")
        
        logging.info("Scraping 4-Hour Workweek jobs...")
        try:
            hw4_jobs = scrape_4hw_jobs()
            all_jobs.extend(hw4_jobs)
        except Exception as e:
            logger.error(f"4HW scraper failed: {e}")
        
        logging.info("Scraping 80,000 Hours jobs...")
        try:
            eighty_k_jobs = scrape_80k_hours_jobs()
            all_jobs.extend(eighty_k_jobs)
        except Exception as e:
            logger.error(f"80k Hours scraper failed: {e}")
        
        logging.info("Scraping Remote OK jobs...")
        try:
            remote_ok_jobs = scrape_remote_ok_jobs()
            all_jobs.extend(remote_ok_jobs)
        except Exception as e:
            logger.error(f"Remote OK scraper failed: {e}")
        
        logging.info(f"Total jobs scraped from all sources: {len(all_jobs)}")
        
        # Save raw data
        data_file = Path('data') / f'jobs_{today}.json'
        with open(data_file, 'w') as f:
            json.dump(all_jobs, f, indent=2)
        logging.info(f"Saved {len(all_jobs)} raw jobs to {data_file}")
        
        # 2. Score and filter jobs
        logging.info("Scoring jobs...")
        scored_jobs = score_jobs_batch(all_jobs)
        logging.info(f"Found {len(scored_jobs)} good matches")
        
        # 3. Generate summary
        summary_file = Path('summaries') / f'{today}.md'
        summary_content = generate_summary(scored_jobs, today)
        summary_file.write_text(summary_content)
        
        logging.info(f"Summary written to {summary_file}")
        print(f"📊 Daily summary generated at {summary_file}")
        print(f"✅ Found {len(scored_jobs)} matching jobs!")
        
    elif args.scrape_only:
        logging.info("Scraping mode")
        # Scrape logic
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()