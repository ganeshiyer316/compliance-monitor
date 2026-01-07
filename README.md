# Compliance Monitor

Automated system for monitoring Visa, Mastercard, PSP, and regulatory changes affecting payment businesses.

## Problem

Payment companies learn about compliance deadlines 2-3 months before they hit, creating expensive fire drills. Example: Visa AFT requirements for March 2026 that most companies learned about in December 2025.

## Solution

This system gives you 6-12 months advance warning by:
- Automatically scraping payment documentation sites
- Detecting changes using content hashing
- Analyzing changes with Claude AI to extract requirements
- Alerting on deadlines, MCCs, regions, and technical requirements

## Features

- **Multi-Agent Architecture**: Scraper, Change Detector, Intelligence, Alert, and Orchestrator agents
- **SQLite Database**: Local persistence with 4 core tables
- **Claude AI Integration**: Intelligent analysis of compliance changes (Opus 4.5 support)
- **Relevance Scoring**: Filters based on your MCCs, regions, and keywords
- **Terminal Alerts**: Color-coded, detailed compliance notifications
- **Interactive Dashboard**: Professional web UI with filters, search, and exports
- **Demo Mode**: Test without API calls using realistic data
- **GitHub Actions**: Automated weekly scans
- **Easy Deployment**: One-click deploy to Vercel or GitHub Pages

## Live Demo

🌐 **Dashboard:** [https://compliance-monitor.vercel.app](https://compliance-monitor.vercel.app)

## Deploy Your Own

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ganeshgunti/compliance-monitor)

### Quick Deploy to Vercel

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Add `ANTHROPIC_API_KEY` environment variable
4. Deploy!

Your dashboard will be live at `https://your-project.vercel.app`

### Deploy to GitHub Pages

1. Fork this repository
2. Go to Settings → Pages
3. Source: Deploy from branch `main`, folder `/dashboard`
4. Add `ANTHROPIC_API_KEY` to repository secrets (Settings → Secrets)
5. Dashboard live at `https://your-username.github.io/compliance-monitor/`

## Quick Start

### 1. Installation

```bash
cd compliance-monitor
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Add your Anthropic API key to .env
# Get key from: https://console.anthropic.com/
```

### 3. Initialize

```bash
python run.py init
```

This creates the database and loads sources from `config/sources.yaml`.

### 4. Test with Demo Data

```bash
python run.py demo
python run.py list
```

This generates 5 realistic compliance items to test the system.

### 5. Run Real Scan

```bash
python run.py scan
```

This will:
1. Scrape all active sources
2. Detect changes from previous scans
3. Analyze changes with Claude AI
4. Display compliance alerts

## Project Structure

```
compliance-monitor/
├── agents/
│   ├── scraper_agent.py          # Web scraping
│   ├── change_detector_agent.py  # Diff detection
│   ├── intelligence_agent.py     # Claude AI analysis
│   ├── alert_agent.py            # Terminal output
│   └── orchestrator.py           # Agent coordination
├── config/
│   ├── sources.yaml              # URLs to monitor
│   ├── company_profile.yaml      # Your MCCs, regions, keywords
│   └── settings.yaml             # System configuration
├── utils/
│   ├── db_utils.py               # Database functions
│   └── demo_data.py              # Demo data generator
├── data/
│   └── compliance.db             # SQLite database
├── logs/
│   └── monitor.log               # Application logs
├── requirements.txt
├── .env.example
├── run.py                        # CLI interface
└── README.md
```

## CLI Commands

```bash
# Initialize database and load sources
python run.py init

# Generate demo data for testing
python run.py demo

# Run full monitoring scan
python run.py scan

# List all compliance items
python run.py list

# Filter by impact level
python run.py list --impact high

# Filter by relevance score
python run.py list --min-relevance 8

# Show statistics
python run.py stats
```

## Configuration

### Add Monitoring Sources

Edit `config/sources.yaml`:

```yaml
sources:
  - name: "Your PSP Documentation"
    url: "https://docs.yourpsp.com/compliance"
    type: "psp_docs"
    active: true
```

### Customize Company Profile

Edit `config/company_profile.yaml`:

```yaml
company:
  name: "Your Company"
  mccs:
    - 6051  # Your MCC codes
  regions:
    - "MENA"
    - "Europe"
  keywords:
    - "AFT"
    - "crypto"
    - "your", "keywords"
```

### Adjust Settings

Edit `config/settings.yaml`:

```yaml
intelligence:
  claude_model: "claude-sonnet-4-20250514"
  max_tokens: 4000

alerts:
  min_relevance_score: 5  # Only show items >= 5
```

## Architecture

### Multi-Agent System

1. **Scraper Agent**
   - Fetches web content using requests/BeautifulSoup
   - Extracts main text content
   - Calculates SHA256 hash
   - Saves snapshots to database

2. **Change Detector Agent**
   - Compares snapshot hashes
   - Generates unified diffs
   - Filters noise (dates, copyright notices)
   - Creates change records

3. **Intelligence Agent**
   - Sends diffs to Claude API
   - Extracts structured data (title, deadline, MCCs, requirements)
   - Calculates relevance scores
   - Creates compliance items

4. **Alert Agent**
   - Queries compliance items
   - Formats with colors and icons
   - Displays in terminal
   - Shows deadlines, requirements, impact

5. **Orchestrator**
   - Coordinates all agents
   - Handles rate limiting
   - Manages errors
   - Logs everything

### Database Schema

**sources**: URLs being monitored
- id, name, url, type, active, created_at, updated_at

**snapshots**: Content snapshots with hashes
- id, source_id, content, content_hash, scraped_at, status, error_message

**changes**: Detected differences
- id, source_id, old_snapshot_id, new_snapshot_id, diff_text, detected_at, analyzed

**compliance_items**: Parsed requirements
- id, change_id, source_id, title, summary, deadline, impact_level, mccs, regions, transaction_types, technical_requirements, keywords, relevance_score, created_at

## Relevance Scoring

Items are scored 1-10 based on:

- **Base**: 5 points
- **MCC Match**: +3 points
- **Region Match**: +2 points (or "Global")
- **Keyword Match**: +1 point (if 3+ keywords match)
- **High Impact**: +1 point
- **Maximum**: 10 points

## Cost

- **Per Scan**: ~$0.50 - $2.00 (depends on number of changes)
- **Monthly**: ~$30 - $60 (daily scans)
- **API**: Claude Sonnet 4 via Anthropic

## Roadmap

### MVP (Current)
- ✅ Multi-agent architecture
- ✅ SQLite database
- ✅ Claude AI integration
- ✅ Terminal alerts
- ✅ Demo data

### Phase 2
- Dashboard (HTML/CSS/JS)
- Timeline view
- JSON export
- Email alerts
- Scheduled scans

### Phase 3
- Multi-user support
- Web configuration UI
- Postgres database
- Hosted deployment
- API access

## Example Output

```
================================================================================
COMPLIANCE ALERT SUMMARY
================================================================================
Total Items: 5 | Displaying: 5
🔴 High: 3 | 🟡 Medium: 2 | 🟢 Low: 0
================================================================================

================================================================================
🔴 HIGH PRIORITY: Visa AFT Recipient Data Requirements
Deadline: 2026-03-31 (85 days)
MCCs: 6051, 6211 | Regions: Global
Transaction Types: AFT, Original Credit

Summary:
  Visa is mandating new recipientDetails fields for all Account Funding
  Transactions (AFT). Merchants must include enhanced recipient information.

Technical Requirements:
  • Add recipientDetails object to AFT API requests
  • Include recipientName, recipientAddress, recipientAccountNumber fields
  • Implement validation for required fields before submission
  • Update error handling for new decline codes
  • Add logging for recipient data validation failures

Relevance Score: 10/10
Source: Nuvei - Card Scheme Programs
https://docs.nuvei.com/documentation/security-docs/risk-guide/schemes-programs/
================================================================================
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Copy `.env.example` to `.env`
- Add your API key from https://console.anthropic.com/

### "Database not found"
- Run `python run.py init` first

### "No active sources found"
- Check `config/sources.yaml` has sources with `active: true`

### Rate limiting / timeouts
- Adjust `rate_limit_seconds` in `config/settings.yaml`
- Increase `timeout_seconds` for slow sites

## Contributing

Contributions welcome! Areas for improvement:
- Additional sources (Visa, Mastercard, regional regulators)
- Better change detection (ML-based filtering)
- Dashboard implementation
- Email/Slack alerting
- Deployment guides

## License

MIT License - Feel free to use for commercial purposes.

## Author

Built by Ganesh Gunti
- Targeting Dubai fintech companies
- Solving real compliance monitoring problems
- Demonstrating multi-agent AI systems

## Contact

Questions? Feedback? Want to hire me?
- GitHub: [Your GitHub]
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

---

**Value Proposition**: This system saves $500K+ per compliance deadline by giving you 12+ months advance warning instead of 3-month fire drills.
