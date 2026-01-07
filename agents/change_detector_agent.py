"""
Change Detector Agent - Detects differences between snapshots.
Responsibilities:
- Compare current snapshot with previous
- Generate unified diff
- Filter noise (dates, timestamps, etc.)
- Create change records
"""

import logging
import difflib
import re
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ChangeDetectorAgent:
    """Agent responsible for detecting changes between snapshots."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the change detector agent.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.noise_patterns = [
            r'\d{4}',  # Years
            r'Copyright.*\d{4}',  # Copyright notices
            r'Last updated:.*',  # Update timestamps
            r'Updated on:.*',  # Update timestamps
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # Dates
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # Dates
        ]

    def _normalize_content(self, content: str) -> List[str]:
        """
        Normalize content by removing noise patterns.

        Args:
            content: Text content

        Returns:
            List of normalized lines
        """
        lines = content.split('\n')
        normalized = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Remove known noise patterns
            normalized_line = line
            for pattern in self.noise_patterns:
                normalized_line = re.sub(pattern, '', normalized_line, flags=re.IGNORECASE)

            # Only add if still has content after normalization
            if normalized_line.strip():
                normalized.append(normalized_line)

        return normalized

    def _generate_diff(self, old_content: str, new_content: str) -> str:
        """
        Generate a unified diff between old and new content.

        Args:
            old_content: Previous content
            new_content: Current content

        Returns:
            Unified diff as string
        """
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            lineterm='',
            n=3  # Context lines
        )

        return '\n'.join(diff)

    def _is_significant_change(self, diff_text: str) -> bool:
        """
        Determine if a change is significant enough to analyze.

        Args:
            diff_text: Diff text

        Returns:
            True if significant, False otherwise
        """
        # Count actual changes (lines starting with + or -)
        diff_lines = diff_text.split('\n')
        change_lines = [line for line in diff_lines if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]

        # Need at least 3 changed lines to be significant
        if len(change_lines) < 3:
            return False

        # Check if changes are just whitespace
        non_whitespace_changes = [line for line in change_lines if line.strip()[1:].strip()]
        if len(non_whitespace_changes) < 2:
            return False

        return True

    def detect_changes(self, source_id: int, old_snapshot: Optional[Dict[str, Any]],
                      new_snapshot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Detect changes between snapshots.

        Args:
            source_id: Source ID
            old_snapshot: Previous snapshot (None if first scan)
            new_snapshot: Current snapshot

        Returns:
            Change data dictionary or None if no significant changes
        """
        # If no previous snapshot, this is the first scan
        if old_snapshot is None:
            logger.info(f"Source {source_id}: First snapshot, no changes to detect")
            return None

        old_hash = old_snapshot['content_hash']
        new_hash = new_snapshot['content_hash']

        # Check if content has changed
        if old_hash == new_hash:
            logger.info(f"Source {source_id}: No changes detected (hash match)")
            return None

        logger.info(f"Source {source_id}: Change detected (hash mismatch)")

        # Generate diff
        old_content = old_snapshot['content']
        new_content = new_snapshot['content']
        diff_text = self._generate_diff(old_content, new_content)

        # Check if change is significant
        if not self._is_significant_change(diff_text):
            logger.info(f"Source {source_id}: Change too minor, skipping")
            return None

        logger.info(f"Source {source_id}: Significant change detected")

        return {
            'source_id': source_id,
            'old_snapshot_id': old_snapshot['id'],
            'new_snapshot_id': new_snapshot['id'],
            'diff_text': diff_text
        }

    def detect_all_changes(self, sources_with_snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect changes for multiple sources.

        Args:
            sources_with_snapshots: List of dicts with 'source_id', 'old_snapshot', 'new_snapshot'

        Returns:
            List of change data dictionaries
        """
        changes = []

        for item in sources_with_snapshots:
            change = self.detect_changes(
                item['source_id'],
                item.get('old_snapshot'),
                item['new_snapshot']
            )

            if change:
                changes.append(change)

        logger.info(f"Detected {len(changes)} significant changes across {len(sources_with_snapshots)} sources")
        return changes

    def get_change_summary(self, diff_text: str, max_lines: int = 50) -> str:
        """
        Get a summary of changes for display.

        Args:
            diff_text: Full diff text
            max_lines: Maximum lines to include

        Returns:
            Summary string
        """
        lines = diff_text.split('\n')

        if len(lines) <= max_lines:
            return diff_text

        # Get first max_lines/2 and last max_lines/2
        half = max_lines // 2
        summary_lines = lines[:half] + [f'\n... ({len(lines) - max_lines} lines omitted) ...\n'] + lines[-half:]

        return '\n'.join(summary_lines)
