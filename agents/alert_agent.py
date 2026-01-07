"""
Alert Agent - Outputs compliance alerts.
Responsibilities:
- Query compliance items from database
- Format and display in terminal with colors
- Show high-priority items
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

logger = logging.getLogger(__name__)


class AlertAgent:
    """Agent responsible for alerting about compliance items."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the alert agent.

        Args:
            config: Configuration with alert settings
        """
        self.terminal_output = config.get('terminal_output', True)
        self.high_priority_only = config.get('high_priority_only', False)
        self.min_relevance = config.get('min_relevance_score', 5)

    def _get_impact_color(self, impact_level: str) -> str:
        """Get color for impact level."""
        if impact_level == 'high':
            return Fore.RED
        elif impact_level == 'medium':
            return Fore.YELLOW
        elif impact_level == 'low':
            return Fore.GREEN
        return Fore.WHITE

    def _get_impact_icon(self, impact_level: str) -> str:
        """Get icon for impact level."""
        if impact_level == 'high':
            return '[H]'
        elif impact_level == 'medium':
            return '[M]'
        elif impact_level == 'low':
            return '[L]'
        return '[ ]'

    def _calculate_days_remaining(self, deadline_str: Optional[str]) -> Optional[int]:
        """Calculate days remaining until deadline."""
        if not deadline_str:
            return None

        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            today = date.today()
            delta = (deadline - today).days
            return delta
        except Exception:
            return None

    def _format_list(self, json_str: str) -> List[str]:
        """Parse JSON string to list."""
        try:
            return json.loads(json_str) if json_str else []
        except Exception:
            return []

    def _format_compliance_item(self, item: Dict[str, Any]) -> str:
        """
        Format a single compliance item for display.

        Args:
            item: Compliance item dictionary

        Returns:
            Formatted string
        """
        impact_level = item.get('impact_level', 'medium')
        color = self._get_impact_color(impact_level)
        icon = self._get_impact_icon(impact_level)

        # Header
        lines = []
        lines.append(f"\n{color}{'=' * 80}{Style.RESET_ALL}")
        lines.append(f"{icon} {color}{impact_level.upper()} PRIORITY{Style.RESET_ALL}: {Fore.CYAN}{item['title']}{Style.RESET_ALL}")

        # Deadline
        deadline = item.get('deadline')
        if deadline:
            days_remaining = self._calculate_days_remaining(deadline)
            if days_remaining is not None:
                if days_remaining < 0:
                    deadline_str = f"{Fore.RED}OVERDUE by {abs(days_remaining)} days{Style.RESET_ALL}"
                elif days_remaining < 30:
                    deadline_str = f"{Fore.RED}Deadline: {deadline} ({days_remaining} days){Style.RESET_ALL}"
                elif days_remaining < 90:
                    deadline_str = f"{Fore.YELLOW}Deadline: {deadline} ({days_remaining} days){Style.RESET_ALL}"
                else:
                    deadline_str = f"Deadline: {deadline} ({days_remaining} days)"
                lines.append(deadline_str)
        else:
            lines.append(f"{Fore.WHITE}Deadline: Not specified{Style.RESET_ALL}")

        # MCCs and Regions
        mccs = self._format_list(item.get('mccs', '[]'))
        regions = self._format_list(item.get('regions', '[]'))
        if mccs or regions:
            mcc_str = f"MCCs: {', '.join(mccs)}" if mccs else ""
            region_str = f"Regions: {', '.join(regions)}" if regions else ""
            separator = " | " if mcc_str and region_str else ""
            lines.append(f"{mcc_str}{separator}{region_str}")

        # Transaction types
        transaction_types = self._format_list(item.get('transaction_types', '[]'))
        if transaction_types:
            lines.append(f"Transaction Types: {', '.join(transaction_types)}")

        # Summary
        if item.get('summary'):
            lines.append(f"\n{Fore.WHITE}Summary:{Style.RESET_ALL}")
            lines.append(f"  {item['summary']}")

        # Technical requirements
        requirements = self._format_list(item.get('technical_requirements', '[]'))
        if requirements:
            lines.append(f"\n{Fore.WHITE}Technical Requirements:{Style.RESET_ALL}")
            for req in requirements[:5]:  # Limit to 5 for display
                lines.append(f"  • {req}")
            if len(requirements) > 5:
                lines.append(f"  ... and {len(requirements) - 5} more")

        # Relevance score
        relevance = item.get('relevance_score', 0)
        lines.append(f"\n{Fore.WHITE}Relevance Score: {relevance}/10{Style.RESET_ALL}")

        # Source
        source_name = item.get('source_name', 'Unknown')
        source_url = item.get('source_url', '')
        lines.append(f"{Fore.WHITE}Source: {source_name}{Style.RESET_ALL}")
        if source_url:
            lines.append(f"{Fore.BLUE}{source_url}{Style.RESET_ALL}")

        lines.append(f"{color}{'=' * 80}{Style.RESET_ALL}")

        return '\n'.join(lines)

    def alert(self, compliance_items: List[Dict[str, Any]]) -> None:
        """
        Display compliance alerts.

        Args:
            compliance_items: List of compliance item dictionaries
        """
        if not compliance_items:
            print(f"\n{Fore.GREEN}✓ No new compliance items to alert on.{Style.RESET_ALL}\n")
            return

        # Filter by settings
        filtered_items = compliance_items

        if self.high_priority_only:
            filtered_items = [item for item in filtered_items if item.get('impact_level') == 'high']

        if self.min_relevance:
            filtered_items = [item for item in filtered_items if item.get('relevance_score', 0) >= self.min_relevance]

        # Sort by deadline (upcoming first) and relevance
        def sort_key(item):
            deadline = item.get('deadline')
            if deadline:
                try:
                    return (0, datetime.strptime(deadline, '%Y-%m-%d'), -item.get('relevance_score', 0))
                except Exception:
                    pass
            return (1, datetime.max, -item.get('relevance_score', 0))

        filtered_items.sort(key=sort_key)

        # Display summary
        total = len(compliance_items)
        filtered = len(filtered_items)
        high = len([i for i in filtered_items if i.get('impact_level') == 'high'])
        medium = len([i for i in filtered_items if i.get('impact_level') == 'medium'])
        low = len([i for i in filtered_items if i.get('impact_level') == 'low'])

        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}COMPLIANCE ALERT SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"Total Items: {total} | Displaying: {filtered}")
        print(f"[HIGH]: {high} | [MEDIUM]: {medium} | [LOW]: {low}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")

        # Display items
        if self.terminal_output:
            for item in filtered_items:
                formatted = self._format_compliance_item(item)
                print(formatted)

        logger.info(f"Displayed {filtered} compliance alerts out of {total} total items")

    def get_summary_stats(self, compliance_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get summary statistics.

        Args:
            compliance_items: List of compliance items

        Returns:
            Statistics dictionary
        """
        stats = {
            'total': len(compliance_items),
            'high': 0,
            'medium': 0,
            'low': 0,
            'with_deadline': 0,
            'urgent': 0  # < 30 days
        }

        for item in compliance_items:
            impact = item.get('impact_level', 'medium')
            if impact == 'high':
                stats['high'] += 1
            elif impact == 'medium':
                stats['medium'] += 1
            elif impact == 'low':
                stats['low'] += 1

            deadline = item.get('deadline')
            if deadline:
                stats['with_deadline'] += 1
                days_remaining = self._calculate_days_remaining(deadline)
                if days_remaining is not None and 0 <= days_remaining < 30:
                    stats['urgent'] += 1

        return stats
