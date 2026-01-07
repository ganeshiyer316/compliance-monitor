# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd compliance-monitor
pip install -r requirements.txt
```

## Step 2: Setup Environment

```bash
# Copy the environment template
copy .env.example .env

# Edit .env and add your Anthropic API key
# Get your key from: https://console.anthropic.com/
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

## Step 3: Initialize Database

```bash
python run.py init
```

This will:
- Create the SQLite database at `data/compliance.db`
- Load 4 monitoring sources from `config/sources.yaml`

## Step 4: Test with Demo Data

```bash
python run.py demo
```

This generates 5 realistic compliance items:
- Visa AFT Recipient Data Requirements
- Mastercard Enhanced Fraud Monitoring
- CBUAE VASP Guidelines
- Visa Direct API v2.0 Migration
- PCI DSS v4.0 Compliance

## Step 5: View the Results

```bash
python run.py list
```

You should see color-coded compliance alerts with:
- 🔴 High priority items
- 🟡 Medium priority items
- Deadlines and days remaining
- MCCs, regions, transaction types
- Technical requirements
- Relevance scores

## Step 6: Run a Real Scan (Optional)

```bash
python run.py scan
```

This will:
1. Scrape all 4 configured sources
2. Compare with previous snapshots
3. Detect changes
4. Analyze with Claude AI (uses API credits)
5. Display new compliance items

**Note**: First scan won't detect changes (no previous snapshots). Run it twice to see change detection.

## Filtering Results

```bash
# Show only high priority items
python run.py list --impact high

# Show items with relevance score >= 8
python run.py list --min-relevance 8

# Show statistics
python run.py stats
```

## Customization

### Add Your Sources

Edit `config/sources.yaml`:

```yaml
sources:
  - name: "Your PSP Documentation"
    url: "https://docs.yourpsp.com/compliance"
    type: "psp_docs"
    active: true
```

Then re-initialize:
```bash
python run.py init
```

### Update Company Profile

Edit `config/company_profile.yaml`:

```yaml
company:
  name: "Your Company Name"
  mccs:
    - 6051  # Your MCC codes
    - 7995  # Add yours
  regions:
    - "MENA"
    - "Your regions"
  keywords:
    - "your"
    - "compliance"
    - "keywords"
```

This affects relevance scoring for alerts.

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the compliance-monitor directory
cd compliance-monitor
python run.py init
```

### API Key Issues
- Verify your API key is correct in `.env`
- Check you have credits at https://console.anthropic.com/

### No Changes Detected
- Run `python run.py scan` twice
- First scan creates baseline snapshots
- Second scan detects changes

## Next Steps

1. **Customize sources**: Add your PSP and regulator URLs
2. **Update profile**: Set your actual MCCs and regions
3. **Schedule scans**: Run daily/weekly via cron or Task Scheduler
4. **Iterate**: The system learns what's relevant to you over time

## Cost

- Demo data: Free (no API calls)
- Real scans: ~$0.50-$2 per scan depending on changes detected
- Recommended: Run weekly to balance cost and coverage

## Support

Questions? Check the full README.md or open an issue.

Happy monitoring!
