"""
CLI Interface for Compliance Monitoring System
Commands:
- init: Initialize database
- scan: Run full monitoring scan
- list: Display compliance items
- demo: Generate demo data
- export: Export compliance items to CSV/HTML
- stats: Show system statistics
"""

import click
import logging
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import db_utils
from utils.demo_data import generate_demo_data
from utils.export_utils import export_to_csv, export_to_html
from agents.orchestrator import Orchestrator
from agents.alert_agent import AlertAgent

# Load environment variables
load_dotenv()


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "monitor.log"),
            logging.StreamHandler()
        ]
    )


def load_config() -> dict:
    """Load configuration from YAML files."""
    config_dir = Path("config")

    # Load settings
    with open(config_dir / "settings.yaml", 'r') as f:
        settings = yaml.safe_load(f)

    # Load company profile
    with open(config_dir / "company_profile.yaml", 'r') as f:
        company_profile = yaml.safe_load(f)

    # Load sources
    with open(config_dir / "sources.yaml", 'r') as f:
        sources = yaml.safe_load(f)

    return {
        'settings': settings,
        'company_profile': company_profile['company'],
        'sources': sources['sources']
    }


def get_db_path(config: dict) -> str:
    """Get database path from config."""
    data_dir = config['settings']['system'].get('data_dir', 'data')
    Path(data_dir).mkdir(exist_ok=True)
    return db_utils.get_db_path(data_dir)


@click.group()
def cli():
    """Compliance Monitoring System - Automated tracking of payment scheme changes."""
    pass


@cli.command()
def init():
    """Initialize the database and load sources."""
    click.echo(f"\n{Fore.CYAN}Initializing Compliance Monitor...{Style.RESET_ALL}\n")

    try:
        # Load config
        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))

        # Initialize database
        db_path = get_db_path(config)
        click.echo(f"Creating database at: {db_path}")
        db_utils.init_database(db_path)

        # Load sources from config
        sources = config['sources']
        click.echo(f"Loading {len(sources)} sources from configuration...")

        for source in sources:
            source_id = db_utils.insert_source(
                db_path,
                source['name'],
                source['url'],
                source['type'],
                source.get('active', True)
            )
            click.echo(f"  [OK] {source['name']}")

        click.echo(f"\n{Fore.GREEN}[OK] Initialization complete!{Style.RESET_ALL}")
        click.echo(f"\nNext steps:")
        click.echo(f"  1. Copy .env.example to .env and add your ANTHROPIC_API_KEY")
        click.echo(f"  2. Run 'python run.py demo' to generate test data")
        click.echo(f"  3. Run 'python run.py scan' to start monitoring")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Initialization failed: {e}{Style.RESET_ALL}")
        logging.error(f"Initialization failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def demo():
    """Generate demo compliance data for testing."""
    click.echo(f"\n{Fore.CYAN}Generating demo data...{Style.RESET_ALL}\n")

    try:
        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Generate demo data
        generate_demo_data(db_path)

        click.echo(f"\n{Fore.GREEN}[OK] Demo data generated successfully!{Style.RESET_ALL}")
        click.echo(f"\nNext step: Run 'python run.py list' to view the demo items")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Demo generation failed: {e}{Style.RESET_ALL}")
        logging.error(f"Demo generation failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def scan():
    """Run a full compliance monitoring scan."""
    click.echo(f"\n{Fore.CYAN}Starting compliance monitoring scan...{Style.RESET_ALL}\n")

    try:
        # Check for API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            click.echo(f"{Fore.RED}[ERROR] ANTHROPIC_API_KEY not found in environment.{Style.RESET_ALL}")
            click.echo(f"  Copy .env.example to .env and add your API key.")
            sys.exit(1)

        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Create orchestrator
        full_config = {
            'scraping': config['settings']['scraping'],
            'intelligence': config['settings']['intelligence'],
            'alerts': config['settings']['alerts']
        }

        orchestrator = Orchestrator(full_config, config['company_profile'], db_path)

        # Run scan
        stats = orchestrator.run_full_scan()

        click.echo(f"\n{Fore.GREEN}[OK] Scan completed successfully!{Style.RESET_ALL}")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Scan failed: {e}{Style.RESET_ALL}")
        logging.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
@click.option('--impact', type=click.Choice(['high', 'medium', 'low']), help='Filter by impact level')
@click.option('--min-relevance', type=int, default=0, help='Minimum relevance score (0-10)')
def list(impact, min_relevance):
    """List all compliance items."""
    try:
        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Create alert agent for display
        alert_config = config['settings']['alerts'].copy()
        alert_config['min_relevance_score'] = min_relevance
        if impact:
            alert_config['high_priority_only'] = (impact == 'high')

        alert_agent = AlertAgent(alert_config)

        # Get items
        items = db_utils.get_compliance_items(
            db_path,
            min_relevance=min_relevance,
            impact_level=impact
        )

        # Display
        alert_agent.alert(items)

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Failed to list items: {e}{Style.RESET_ALL}")
        logging.error(f"List failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def stats():
    """Show system statistics."""
    try:
        config = load_config()
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Get statistics
        items = db_utils.get_compliance_items(db_path, min_relevance=0)
        alert_agent = AlertAgent(config['settings']['alerts'])
        stats = alert_agent.get_summary_stats(items)

        click.echo(f"\n{Fore.CYAN}=== Compliance Monitor Statistics ==={Style.RESET_ALL}\n")
        click.echo(f"Total Items: {stats['total']}")
        click.echo(f"[HIGH] High Priority: {stats['high']}")
        click.echo(f"[MEDIUM] Medium Priority: {stats['medium']}")
        click.echo(f"[LOW] Low Priority: {stats['low']}")
        click.echo(f"\nItems with Deadline: {stats['with_deadline']}")
        click.echo(f"Urgent (< 30 days): {stats['urgent']}\n")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Failed to get statistics: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
@click.option('--format', type=click.Choice(['csv', 'html', 'both']), default='both', help='Export format')
@click.option('--impact', type=click.Choice(['high', 'medium', 'low']), help='Filter by impact level')
@click.option('--min-relevance', type=int, default=0, help='Minimum relevance score (0-10)')
@click.option('--output-dir', default='exports', help='Output directory for exports')
def export(format, impact, min_relevance, output_dir):
    """Export compliance items to CSV and/or HTML format."""
    click.echo(f"\n{Fore.CYAN}Exporting compliance data...{Style.RESET_ALL}\n")

    try:
        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Get items
        items = db_utils.get_compliance_items(
            db_path,
            min_relevance=min_relevance,
            impact_level=impact
        )

        if not items:
            click.echo(f"{Fore.YELLOW}No compliance items found matching your criteria.{Style.RESET_ALL}")
            sys.exit(0)

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        exported_files = []

        # Export to CSV
        if format in ['csv', 'both']:
            csv_file = output_path / f'compliance_report_{timestamp}.csv'
            export_to_csv(items, str(csv_file))
            exported_files.append(str(csv_file))
            click.echo(f"{Fore.GREEN}[OK] CSV exported: {csv_file}{Style.RESET_ALL}")

        # Export to HTML
        if format in ['html', 'both']:
            html_file = output_path / f'compliance_report_{timestamp}.html'
            export_to_html(items, str(html_file))
            exported_files.append(str(html_file))
            click.echo(f"{Fore.GREEN}[OK] HTML exported: {html_file}{Style.RESET_ALL}")

        click.echo(f"\n{Fore.GREEN}[OK] Export completed successfully!{Style.RESET_ALL}")
        click.echo(f"Exported {len(items)} items to {len(exported_files)} file(s)")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Export failed: {e}{Style.RESET_ALL}")
        logging.error(f"Export failed: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def dashboard():
    """Generate dashboard data and open in browser."""
    import json

    click.echo(f"\n{Fore.CYAN}Generating dashboard...{Style.RESET_ALL}\n")

    try:
        config = load_config()
        setup_logging(config['settings']['system'].get('log_level', 'INFO'))
        db_path = get_db_path(config)

        # Check if database exists
        if not os.path.exists(db_path):
            click.echo(f"{Fore.RED}[ERROR] Database not found. Run 'python run.py init' first.{Style.RESET_ALL}")
            sys.exit(1)

        # Get all items
        items = db_utils.get_compliance_items(db_path, min_relevance=0)

        if not items:
            click.echo(f"{Fore.YELLOW}No compliance items found. Run 'python run.py demo' to generate test data.{Style.RESET_ALL}")
            sys.exit(0)

        # Prepare data for dashboard
        dashboard_data = {
            'last_updated': datetime.now().isoformat(),
            'total_items': len(items),
            'items': items
        }

        # Create dashboard directory if it doesn't exist
        dashboard_dir = Path('dashboard')
        dashboard_dir.mkdir(exist_ok=True)

        # Export to JSON
        json_file = dashboard_dir / 'data.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

        click.echo(f"{Fore.GREEN}[OK] Dashboard data exported: {json_file}{Style.RESET_ALL}")
        click.echo(f"Total items: {len(items)}")
        click.echo(f"\nOpen dashboard/index.html in your browser")

    except Exception as e:
        click.echo(f"\n{Fore.RED}[ERROR] Dashboard generation failed: {e}{Style.RESET_ALL}")
        logging.error(f"Dashboard generation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
