# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based job search agent designed to automate job hunting workflows. The project is in its early stages.

## Project Structure

The repository follows a modular architecture with separated concerns:

- **scrapers/**: Job board scrapers for gathering job listings from various sources
- **analyzers/**: Analysis modules for processing and evaluating job postings
- **data/**: Storage for scraped job data and structured datasets
- **logs/**: Application logs and debug output
- **summaries/**: Generated summaries and reports from analyzed jobs
- **main.py**: Entry point for the application

## Development Commands

### Running the Application
```bash
python main.py
```

### Managing Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

### Testing
(To be defined as tests are added to the project)

## Architecture Patterns

When implementing scrapers:
- Each scraper should be a separate module in `scrapers/`
- Scrapers should handle rate limiting and respect robots.txt
- Output data to `data/` in a consistent JSON format

When implementing analyzers:
- Analyzers should read from `data/` and process job postings
- Results should be written to `summaries/`
- Keep analysis logic separate from data collection

## Key Considerations

- All scraped data should be stored locally in `data/`
- Logs should be written to `logs/` with appropriate log levels
- The project structure separates data collection (scrapers) from data processing (analyzers)
