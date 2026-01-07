"""
Intelligence Agent - Uses Claude API to analyze changes.
Responsibilities:
- Send diffs to Claude API
- Extract structured compliance data
- Calculate relevance scores
- Create compliance items
"""

import logging
import json
import os
from typing import Dict, Any, Optional, List
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class IntelligenceAgent:
    """Agent responsible for analyzing changes using Claude AI."""

    def __init__(self, config: Dict[str, Any], company_profile: Dict[str, Any]):
        """
        Initialize the intelligence agent.

        Args:
            config: Configuration with Claude settings
            company_profile: Company profile for relevance scoring
        """
        self.model = config.get('claude_model', 'claude-sonnet-4-20250514')
        self.max_tokens = config.get('max_tokens', 4000)
        self.temperature = config.get('temperature', 0.1)
        self.company_profile = company_profile

        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=api_key)

    def _create_analysis_prompt(self, diff_text: str, source_name: str, source_url: str) -> str:
        """
        Create prompt for Claude to analyze the change.

        Args:
            diff_text: Diff text showing changes
            source_name: Name of the source
            source_url: URL of the source

        Returns:
            Formatted prompt
        """
        prompt = f"""You are a compliance expert analyzing changes to payment industry documentation.

Source: {source_name}
URL: {source_url}

Below is a diff showing changes detected on this page. Analyze this change and extract compliance-relevant information.

DIFF:
{diff_text}

Extract the following information and return ONLY a valid JSON object (no markdown, no explanation):

{{
  "title": "Brief title of the compliance change",
  "summary": "2-3 sentence summary of what changed and why it matters",
  "deadline": "YYYY-MM-DD format if deadline mentioned, or null",
  "impact_level": "high|medium|low",
  "mccs": ["list", "of", "MCC", "codes", "if", "mentioned"],
  "regions": ["list", "of", "regions", "like", "Global", "MENA", "Europe"],
  "transaction_types": ["AFT", "OCT", "etc"],
  "technical_requirements": ["list", "of", "technical", "requirements"],
  "keywords": ["relevant", "keywords"]
}}

Guidelines:
- If no deadline is mentioned, use null
- impact_level: "high" if requires code changes, "medium" if requires process changes, "low" if informational
- Include all relevant MCCs, regions, transaction types
- Extract 5-10 relevant keywords
- Be concise and technical

Return ONLY the JSON object, nothing else."""

        return prompt

    def _parse_claude_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse Claude's response into structured data.

        Args:
            response_text: Response from Claude

        Returns:
            Parsed data dictionary or None if failed
        """
        try:
            # Try to extract JSON from response
            # Sometimes Claude wraps it in markdown code blocks
            text = response_text.strip()

            # Remove markdown code blocks if present
            if text.startswith('```'):
                lines = text.split('\n')
                text = '\n'.join(lines[1:-1]) if len(lines) > 2 else text

            # Remove leading "json" if present
            if text.startswith('json'):
                text = text[4:].strip()

            data = json.loads(text)
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            logger.debug(f"Response was: {response_text}")
            return None

    def _calculate_relevance_score(self, analysis: Dict[str, Any]) -> int:
        """
        Calculate relevance score (1-10) based on company profile.

        Args:
            analysis: Analyzed compliance data

        Returns:
            Relevance score 1-10
        """
        score = 5  # Base score

        # Check MCC match
        company_mccs = set(str(mcc) for mcc in self.company_profile.get('mccs', []))
        item_mccs = set(analysis.get('mccs', []))
        if company_mccs & item_mccs:
            score += 3
            logger.debug(f"MCC match: +3 points")

        # Check region match
        company_regions = set(r.upper() for r in self.company_profile.get('regions', []))
        item_regions = set(r.upper() for r in analysis.get('regions', []))
        if company_regions & item_regions or 'GLOBAL' in item_regions:
            score += 2
            logger.debug(f"Region match: +2 points")

        # Check keyword match
        company_keywords = set(k.lower() for k in self.company_profile.get('keywords', []))
        item_keywords = set(k.lower() for k in analysis.get('keywords', []))
        keyword_matches = len(company_keywords & item_keywords)
        if keyword_matches >= 3:
            score += 1
            logger.debug(f"Keyword match ({keyword_matches}): +1 point")

        # Check impact level
        if analysis.get('impact_level') == 'high':
            score += 1
            logger.debug(f"High impact: +1 point")

        # Cap at 10
        score = min(score, 10)

        logger.info(f"Calculated relevance score: {score}/10")
        return score

    def analyze_change(self, change: Dict[str, Any], source_name: str, source_url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a change using Claude API.

        Args:
            change: Change data with diff_text
            source_name: Name of the source
            source_url: URL of the source

        Returns:
            Compliance item data or None if analysis failed
        """
        change_id = change.get('id')
        diff_text = change['diff_text']

        logger.info(f"Analyzing change {change_id} from {source_name}")

        try:
            # Create prompt
            prompt = self._create_analysis_prompt(diff_text, source_name, source_url)

            # Call Claude API
            logger.debug(f"Calling Claude API with model {self.model}")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract response
            response_text = message.content[0].text
            logger.debug(f"Received response from Claude ({len(response_text)} chars)")

            # Parse response
            analysis = self._parse_claude_response(response_text)
            if not analysis:
                logger.error(f"Failed to parse Claude response for change {change_id}")
                return None

            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(analysis)

            # Convert lists to JSON strings for database storage
            compliance_item = {
                'title': analysis.get('title', 'Untitled Change'),
                'summary': analysis.get('summary', ''),
                'deadline': analysis.get('deadline'),
                'impact_level': analysis.get('impact_level', 'medium'),
                'mccs': json.dumps(analysis.get('mccs', [])),
                'regions': json.dumps(analysis.get('regions', [])),
                'transaction_types': json.dumps(analysis.get('transaction_types', [])),
                'technical_requirements': json.dumps(analysis.get('technical_requirements', [])),
                'keywords': json.dumps(analysis.get('keywords', [])),
                'relevance_score': relevance_score
            }

            logger.info(f"Successfully analyzed change {change_id}: {compliance_item['title']} (relevance: {relevance_score})")

            return compliance_item

        except Exception as e:
            logger.error(f"Failed to analyze change {change_id}: {e}", exc_info=True)
            return None

    def analyze_all_changes(self, changes: List[Dict[str, Any]], sources_map: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple changes.

        Args:
            changes: List of change dictionaries
            sources_map: Map of source_id to source data

        Returns:
            List of tuples (change_id, source_id, compliance_item_data)
        """
        results = []

        for change in changes:
            source_id = change['source_id']
            source = sources_map.get(source_id, {})
            source_name = source.get('name', 'Unknown')
            source_url = source.get('url', '')

            compliance_item = self.analyze_change(change, source_name, source_url)

            if compliance_item:
                results.append({
                    'change_id': change['id'],
                    'source_id': source_id,
                    'compliance_item': compliance_item
                })

        logger.info(f"Analyzed {len(results)} changes successfully out of {len(changes)}")
        return results
