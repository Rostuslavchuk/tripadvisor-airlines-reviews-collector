# Tripadvisor Airline Reviews Scraper

A Python-based scraper that collects available airline reviews from [Tripadvisor Airlines](https://www.tripadvisor.com/Airlines).

## Features

- Collects airline reviews from Tripadvisor.
- Extracts review data using the Tripadvisor Reviews API.
- Uses Playwright to initialize browser sessions and collect cookies.
- Uses `curl_cffi` for asynchronous HTTP requests.
- Parses and validates extracted data with Pydantic.
- Supports asynchronous processing with `asyncio`.
- Exports collected reviews to JSON.

## Tech Stack

- **Python**
- **Playwright** – browser automation and cookie collection.
- **curl_cffi** – HTTP requests with browser impersonation.
- **asyncio** – asynchronous execution.
- **Pydantic** – data validation.
- **lxml / XPath** – HTML parsing.

## Project Structure

```text
.
├── config/
│   └── headers.py
├── fetcher/
│   └── fetcher.py
├── models/
│   └── reviews_model.py
├── parser/
│   └── parser.py
├── piplines/
│   └── reviews_pipline.py
├── storage/
│   └── scheduler.py
├── utils/
│   └── logger.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd tripadvisor-reviews-scraper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Chromium:

```bash
playwright install chromium
```

## Usage

Run the scraper from the project root:

```bash
python -m piplines.reviews_pipline -u "https://www.tripadvisor.com/Airline_Review-d8728874-Reviews-Aeromar"
```

Replace the URL with the Tripadvisor airline page you want to scrape.

## Output

Collected reviews are validated and exported to JSON.

## Disclaimer

This project is intended for educational and research purposes. Use responsibly and respect Tripadvisor's Terms of Service and applicable rate limits.
