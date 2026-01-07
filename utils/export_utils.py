"""
Export utilities for compliance monitoring data
Supports CSV and HTML export formats
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def export_to_csv(items: List[Dict[str, Any]], output_path: str) -> str:
    """
    Export compliance items to CSV format.

    Args:
        items: List of compliance items
        output_path: Path to save CSV file

    Returns:
        Path to created CSV file
    """
    if not items:
        raise ValueError("No items to export")

    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Define CSV columns
    fieldnames = [
        'title',
        'impact_level',
        'deadline',
        'days_remaining',
        'summary',
        'mccs',
        'regions',
        'transaction_types',
        'technical_requirements',
        'relevance_score',
        'source_name',
        'url',
        'detected_at'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in items:
            # Calculate days remaining
            days_remaining = ''
            if item.get('deadline'):
                try:
                    deadline = datetime.fromisoformat(item['deadline'])
                    days = (deadline - datetime.now()).days
                    days_remaining = str(days)
                except:
                    pass

            # Parse JSON fields if they're strings
            def parse_field(field_value):
                if isinstance(field_value, str):
                    try:
                        return json.loads(field_value)
                    except:
                        return field_value
                return field_value if field_value else []

            mccs = parse_field(item.get('mccs', []))
            regions = parse_field(item.get('regions', []))
            transaction_types = parse_field(item.get('transaction_types', []))
            technical_requirements = parse_field(item.get('technical_requirements', []))

            # Format lists as comma-separated strings
            row = {
                'title': item.get('title', ''),
                'impact_level': item.get('impact_level', '').upper(),
                'deadline': item.get('deadline', ''),
                'days_remaining': days_remaining,
                'summary': item.get('summary', ''),
                'mccs': ', '.join(map(str, mccs)) if isinstance(mccs, list) else str(mccs),
                'regions': ', '.join(regions) if isinstance(regions, list) else str(regions),
                'transaction_types': ', '.join(transaction_types) if isinstance(transaction_types, list) else str(transaction_types),
                'technical_requirements': ' | '.join(technical_requirements) if isinstance(technical_requirements, list) else str(technical_requirements),
                'relevance_score': item.get('relevance_score', ''),
                'source_name': item.get('source_name', ''),
                'url': item.get('url', ''),
                'detected_at': item.get('detected_at', '')
            }
            writer.writerow(row)

    return str(output_file)


def export_to_html(items: List[Dict[str, Any]], output_path: str) -> str:
    """
    Export compliance items to HTML report format.

    Args:
        items: List of compliance items
        output_path: Path to save HTML file

    Returns:
        Path to created HTML file
    """
    if not items:
        raise ValueError("No items to export")

    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate HTML content
    html_content = generate_html_report(items)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return str(output_file)


def generate_html_report(items: List[Dict[str, Any]]) -> str:
    """Generate HTML report content."""

    # Calculate statistics
    total = len(items)
    high = len([i for i in items if i.get('impact_level') == 'high'])
    medium = len([i for i in items if i.get('impact_level') == 'medium'])
    low = len([i for i in items if i.get('impact_level') == 'low'])

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Start HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compliance Alert Report - {timestamp}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .header .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .high {{ color: #e74c3c; }}
        .medium {{ color: #f39c12; }}
        .low {{ color: #27ae60; }}
        .item {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 5px solid #ccc;
        }}
        .item.high {{ border-left-color: #e74c3c; }}
        .item.medium {{ border-left-color: #f39c12; }}
        .item.low {{ border-left-color: #27ae60; }}
        .item-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        .item-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin: 0;
        }}
        .priority-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        .priority-badge.high {{ background-color: #e74c3c; }}
        .priority-badge.medium {{ background-color: #f39c12; }}
        .priority-badge.low {{ background-color: #27ae60; }}
        .item-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .meta-item {{
            font-size: 0.9em;
        }}
        .meta-label {{
            font-weight: bold;
            color: #555;
        }}
        .deadline {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .summary-text {{
            margin: 15px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            line-height: 1.8;
        }}
        .tech-requirements {{
            margin: 15px 0;
        }}
        .tech-requirements h4 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .tech-requirements ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .tech-requirements li {{
            margin: 5px 0;
            line-height: 1.6;
        }}
        .relevance-score {{
            display: inline-block;
            padding: 5px 10px;
            background-color: #667eea;
            color: white;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 10px;
        }}
        .source-link {{
            color: #667eea;
            text-decoration: none;
            font-size: 0.9em;
        }}
        .source-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Compliance Alert Report</h1>
        <div class="timestamp">Generated: {timestamp}</div>
    </div>

    <div class="summary">
        <div class="summary-card">
            <div class="label">Total Items</div>
            <div class="number">{total}</div>
        </div>
        <div class="summary-card">
            <div class="label">High Priority</div>
            <div class="number high">{high}</div>
        </div>
        <div class="summary-card">
            <div class="label">Medium Priority</div>
            <div class="number medium">{medium}</div>
        </div>
        <div class="summary-card">
            <div class="label">Low Priority</div>
            <div class="number low">{low}</div>
        </div>
    </div>
"""

    # Helper function to parse JSON fields
    def parse_field(field_value):
        if isinstance(field_value, str):
            try:
                return json.loads(field_value)
            except:
                return field_value
        return field_value if field_value else []

    # Add each compliance item
    for item in items:
        impact_level = item.get('impact_level', 'low')
        title = item.get('title', 'Untitled')
        summary = item.get('summary', 'No summary available')
        deadline = item.get('deadline', 'No deadline')

        # Calculate days remaining
        days_text = ''
        if deadline != 'No deadline':
            try:
                deadline_date = datetime.fromisoformat(deadline)
                days = (deadline_date - datetime.now()).days
                days_text = f' ({days} days)'
            except:
                pass

        # Parse and format metadata
        mccs_list = parse_field(item.get('mccs', []))
        regions_list = parse_field(item.get('regions', []))
        transaction_types_list = parse_field(item.get('transaction_types', []))

        mccs = ', '.join(map(str, mccs_list)) if isinstance(mccs_list, list) else str(mccs_list) or 'N/A'
        regions = ', '.join(regions_list) if isinstance(regions_list, list) else str(regions_list) or 'N/A'
        transaction_types = ', '.join(transaction_types_list) if isinstance(transaction_types_list, list) else str(transaction_types_list) or 'N/A'

        # Technical requirements
        tech_reqs = parse_field(item.get('technical_requirements', []))
        tech_reqs_html = ''
        if tech_reqs and isinstance(tech_reqs, list):
            tech_reqs_html = '<div class="tech-requirements"><h4>Technical Requirements:</h4><ul>'
            for req in tech_reqs:
                tech_reqs_html += f'<li>{req}</li>'
            tech_reqs_html += '</ul></div>'

        # Relevance score
        relevance = item.get('relevance_score', 'N/A')

        # Source
        source_name = item.get('source_name', 'Unknown')
        url = item.get('url', '#')

        html += f"""
    <div class="item {impact_level}">
        <div class="item-header">
            <h2 class="item-title">{title}</h2>
            <span class="priority-badge {impact_level}">{impact_level.upper()}</span>
        </div>

        <div class="item-meta">
            <div class="meta-item">
                <span class="meta-label">Deadline:</span>
                <span class="deadline">{deadline}{days_text}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">MCCs:</span> {mccs}
            </div>
            <div class="meta-item">
                <span class="meta-label">Regions:</span> {regions}
            </div>
            <div class="meta-item">
                <span class="meta-label">Transaction Types:</span> {transaction_types}
            </div>
        </div>

        <div class="summary-text">
            {summary}
        </div>

        {tech_reqs_html}

        <div>
            <span class="relevance-score">Relevance: {relevance}/10</span>
        </div>

        <div style="margin-top: 15px;">
            <span class="meta-label">Source:</span>
            <a href="{url}" class="source-link" target="_blank">{source_name}</a>
        </div>
    </div>
"""

    # Close HTML
    html += """
    <div class="footer">
        <p>Compliance Monitoring System - Automated tracking of payment scheme changes</p>
    </div>
</body>
</html>
"""

    return html
