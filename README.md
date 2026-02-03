# Job Search Agent

An automated job search assistant that searches job boards daily and creates personalized summaries.

## What This Does

🤖 **Automated Daily Searches**: Runs every day at 8am UTC (midnight PST)
📊 **Smart Analysis**: Scores jobs based on fit and likelihood
📝 **Daily Summaries**: Creates reports showing the best opportunities
☁️ **Cloud-Based**: Runs on GitHub Actions (free!) - your computer can be off

## Project Structure

```
job-search-agent/
├── scrapers/          # Code to search job websites
├── analyzers/         # Code to evaluate job postings
├── summaries/         # Daily reports (auto-generated)
├── data/              # Raw job data
├── logs/              # Activity logs
└── main.py           # Main entry point
```

## Setup Status

✅ GitHub repository created
✅ Python dependencies configured
✅ GitHub Actions workflow ready
✅ Warp environment created
✅ OpenAI API key configured
✅ Job scrapers built (7 sources)
✅ Job analyzer/scorer built
✅ Automated daily runs configured

## How to Use

### Run Manually (Testing)
```bash
python main.py --daily-summary
```

### View Daily Summaries
Check the `summaries/` folder for daily reports, automatically committed to this repo.

## Next Steps

1. Add your OpenAI API key to GitHub Secrets
2. Build scrapers for target companies
3. Create analysis logic for scoring jobs
4. Test the workflow manually on GitHub
5. Let it run automatically every day!

## Job Sources

The agent scrapes from 7 major job boards daily:

1. **LinkedIn** - Remote jobs in US
2. **Indeed** - Remote positions
3. **Wellfound** (formerly AngelList) - Startup jobs
4. **Y Combinator** - YC company jobs
5. **4-Hour Workweek** - Tim Ferriss job board
6. **80,000 Hours** - Impact-focused careers
7. **Remote OK** - Remote-first companies

## Job Criteria

**Target Roles:**
- Customer Operations Manager
- Customer Experience Manager/Lead
- Product Manager (Operations/Internal Tools)
- Implementation Manager
- Operations Manager

**Must-Have:**
- ✅ Remote ONLY (non-negotiable)
- ✅ US timezones
- ✅ Early-stage startups preferred

**Target Industries:**
- Fintech/Payments
- Cannabis/Hemp
- Outdoor recreation, Wellness, Fitness
- E-commerce, SaaS
- And 15+ other industries

## Tech Stack

- **Python 3.11**
- **BeautifulSoup4**: Web scraping
- **Selenium**: Dynamic website scraping
- **OpenAI API**: Job analysis and summaries
- **GitHub Actions**: Automated daily runs
