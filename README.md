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
⏭️ Add OpenAI API key to GitHub Secrets
⏭️ Build job scrapers
⏭️ Build job analyzers

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

## Tech Stack

- **Python 3.11**
- **BeautifulSoup4**: Web scraping
- **Selenium**: Dynamic website scraping
- **OpenAI API**: Job analysis and summaries
- **GitHub Actions**: Automated daily runs