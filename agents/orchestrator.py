"""
Orchestrator - Coordinates all agents in the monitoring pipeline.
Responsibilities:
- Load configuration
- Run agents in sequence
- Handle errors and logging
- Coordinate the full scan workflow
"""

import logging
import os
from typing import Dict, Any, List
from datetime import datetime

from agents.scraper_agent import ScraperAgent
from agents.change_detector_agent import ChangeDetectorAgent
from agents.intelligence_agent import IntelligenceAgent
from agents.alert_agent import AlertAgent
from utils import db_utils

logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestrator for the compliance monitoring system."""

    def __init__(self, config: Dict[str, Any], company_profile: Dict[str, Any], db_path: str):
        """
        Initialize the orchestrator.

        Args:
            config: Full configuration dictionary
            company_profile: Company profile for relevance scoring
            db_path: Path to SQLite database
        """
        self.config = config
        self.company_profile = company_profile
        self.db_path = db_path

        # Initialize agents
        self.scraper = ScraperAgent(config['scraping'])
        self.change_detector = ChangeDetectorAgent()
        self.intelligence = IntelligenceAgent(config['intelligence'], company_profile)
        self.alert = AlertAgent(config['alerts'])

        logger.info("Orchestrator initialized")

    def run_full_scan(self) -> Dict[str, Any]:
        """
        Run a complete monitoring scan.

        Workflow:
        1. Get active sources from database
        2. Scrape all sources (ScraperAgent)
        3. Save snapshots to database
        4. Detect changes (ChangeDetectorAgent)
        5. Analyze changes with Claude (IntelligenceAgent)
        6. Display alerts (AlertAgent)

        Returns:
            Summary statistics
        """
        logger.info("=" * 80)
        logger.info("Starting full compliance monitoring scan")
        logger.info("=" * 80)

        start_time = datetime.now()
        stats = {
            'sources_scanned': 0,
            'snapshots_saved': 0,
            'changes_detected': 0,
            'compliance_items_created': 0,
            'errors': 0
        }

        try:
            # Step 1: Get active sources
            logger.info("Step 1: Loading active sources from database")
            sources = db_utils.get_active_sources(self.db_path)
            logger.info(f"Found {len(sources)} active sources")

            if not sources:
                logger.warning("No active sources found. Add sources to config/sources.yaml and run 'python run.py init'")
                return stats

            # Step 2: Scrape all sources
            logger.info("Step 2: Scraping all sources")
            scrape_results = self.scraper.scrape_all(sources)
            stats['sources_scanned'] = len(scrape_results)

            # Step 3: Save snapshots and prepare for change detection
            logger.info("Step 3: Saving snapshots to database")
            sources_with_snapshots = []

            for result in scrape_results:
                if result['status'] == 'success':
                    # Save snapshot
                    snapshot_id = db_utils.insert_snapshot(
                        self.db_path,
                        result['source_id'],
                        result['content'],
                        result['content_hash'],
                        result['status'],
                        result['error_message']
                    )
                    stats['snapshots_saved'] += 1

                    # Get previous snapshot for comparison
                    old_snapshot = db_utils.get_latest_snapshot(self.db_path, result['source_id'])

                    # Get current snapshot (the one we just saved)
                    new_snapshot = {
                        'id': snapshot_id,
                        'source_id': result['source_id'],
                        'content': result['content'],
                        'content_hash': result['content_hash']
                    }

                    # Check if old_snapshot is the same as new (just saved)
                    if old_snapshot and old_snapshot['id'] == snapshot_id:
                        # This means there was no previous snapshot, so old should be None
                        old_snapshot = None

                    # If old_snapshot exists and has same ID, we need to get the one before it
                    if old_snapshot and old_snapshot['content_hash'] == new_snapshot['content_hash']:
                        # Same hash, try to get older one
                        # For simplicity in MVP, we'll just set old to None for first run
                        pass

                    sources_with_snapshots.append({
                        'source_id': result['source_id'],
                        'old_snapshot': old_snapshot,
                        'new_snapshot': new_snapshot
                    })
                else:
                    stats['errors'] += 1
                    logger.error(f"Failed to scrape source {result['source_id']}: {result.get('error_message')}")

            # Step 4: Detect changes
            logger.info("Step 4: Detecting changes")
            changes = self.change_detector.detect_all_changes(sources_with_snapshots)
            stats['changes_detected'] = len(changes)

            if not changes:
                logger.info("No significant changes detected")
                # Still show existing compliance items
                self._display_existing_alerts()
                return stats

            logger.info(f"Detected {len(changes)} significant changes")

            # Save changes to database
            for change in changes:
                change_id = db_utils.insert_change(
                    self.db_path,
                    change['source_id'],
                    change['old_snapshot_id'],
                    change['new_snapshot_id'],
                    change['diff_text']
                )
                change['id'] = change_id

            # Step 5: Analyze changes with Claude
            logger.info("Step 5: Analyzing changes with Claude AI")

            # Create sources map for intelligence agent
            sources_map = {s['id']: s for s in sources}

            analysis_results = self.intelligence.analyze_all_changes(changes, sources_map)

            # Save compliance items to database
            for result in analysis_results:
                item_id = db_utils.insert_compliance_item(
                    self.db_path,
                    result['change_id'],
                    result['source_id'],
                    result['compliance_item']
                )
                stats['compliance_items_created'] += 1

                # Mark change as analyzed
                db_utils.mark_change_analyzed(self.db_path, result['change_id'])

            # Step 6: Display alerts
            logger.info("Step 6: Displaying alerts")
            self._display_existing_alerts()

        except Exception as e:
            logger.error(f"Error during scan: {e}", exc_info=True)
            stats['errors'] += 1
            raise

        finally:
            # Log summary
            duration = (datetime.now() - start_time).total_seconds()
            logger.info("=" * 80)
            logger.info("Scan completed")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Sources scanned: {stats['sources_scanned']}")
            logger.info(f"Snapshots saved: {stats['snapshots_saved']}")
            logger.info(f"Changes detected: {stats['changes_detected']}")
            logger.info(f"Compliance items created: {stats['compliance_items_created']}")
            logger.info(f"Errors: {stats['errors']}")
            logger.info("=" * 80)

        return stats

    def _display_existing_alerts(self) -> None:
        """Display all compliance items from database."""
        min_relevance = self.config['alerts'].get('min_relevance_score', 5)
        compliance_items = db_utils.get_compliance_items(
            self.db_path,
            min_relevance=min_relevance
        )

        self.alert.alert(compliance_items)

    def list_compliance_items(self, impact_level: str = None, min_relevance: int = 0) -> List[Dict[str, Any]]:
        """
        List compliance items with optional filtering.

        Args:
            impact_level: Filter by impact level (high/medium/low)
            min_relevance: Minimum relevance score

        Returns:
            List of compliance items
        """
        items = db_utils.get_compliance_items(
            self.db_path,
            min_relevance=min_relevance,
            impact_level=impact_level
        )
        return items

    def get_stats(self) -> Dict[str, Any]:
        """
        Get current statistics.

        Returns:
            Statistics dictionary
        """
        all_items = db_utils.get_compliance_items(self.db_path, min_relevance=0)
        stats = self.alert.get_summary_stats(all_items)
        return stats
