"""
Scraper Agent - Fetches web content and saves snapshots.
Responsibilities:
- Fetch URL content
- Extract main text content
- Calculate SHA256 hash
- Save to snapshots table
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ScraperAgent:
    """Agent responsible for scraping web content."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the scraper agent.

        Args:
            config: Configuration dictionary with scraping settings
        """
        self.timeout = config.get('timeout_seconds', 30)
        self.user_agent = config.get('user_agent', 'ComplianceMonitor/1.0')
        self.rate_limit = config.get('rate_limit_seconds', 3)
        self.max_retries = config.get('max_retries', 3)
        self.last_request_time = 0

    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def _fetch_url(self, url: str) -> Optional[str]:
        """
        Fetch content from a URL with retries.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None if failed
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.max_retries})")
                response = requests.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response.text

            except requests.exceptions.RequestException as e:
                logger.warning(f"Fetch attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None

        return None

    def _extract_content(self, html: str) -> str:
        """
        Extract main text content from HTML.

        Args:
            html: Raw HTML content

        Returns:
            Cleaned text content
        """
        soup = BeautifulSoup(html, 'lxml')

        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        # Try to find main content area
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_=['content', 'main-content', 'article-content']) or
            soup.find('body')
        )

        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)

        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)

        return cleaned_text

    def _calculate_hash(self, content: str) -> str:
        """
        Calculate SHA256 hash of content.

        Args:
            content: Text content

        Returns:
            Hex digest of hash
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def scrape(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape a source and return snapshot data.

        Args:
            source: Source dictionary with 'url', 'name', etc.

        Returns:
            Dictionary with scraping results
        """
        source_id = source['id']
        url = source['url']
        name = source['name']

        logger.info(f"Scraping source: {name}")

        # Enforce rate limiting
        self._rate_limit()

        # Fetch content
        html = self._fetch_url(url)

        if html is None:
            logger.error(f"Failed to scrape {name}")
            return {
                'source_id': source_id,
                'content': '',
                'content_hash': '',
                'status': 'error',
                'error_message': 'Failed to fetch URL'
            }

        # Extract text content
        try:
            content = self._extract_content(html)
            content_hash = self._calculate_hash(content)

            logger.info(f"Successfully scraped {name} ({len(content)} chars, hash: {content_hash[:16]}...)")

            return {
                'source_id': source_id,
                'content': content,
                'content_hash': content_hash,
                'status': 'success',
                'error_message': None
            }

        except Exception as e:
            logger.error(f"Failed to extract content from {name}: {e}")
            return {
                'source_id': source_id,
                'content': '',
                'content_hash': '',
                'status': 'error',
                'error_message': str(e)
            }

    def scrape_all(self, sources: list) -> list:
        """
        Scrape multiple sources.

        Args:
            sources: List of source dictionaries

        Returns:
            List of snapshot results
        """
        results = []

        for source in sources:
            result = self.scrape(source)
            results.append(result)

        logger.info(f"Scraped {len(results)} sources")
        return results
