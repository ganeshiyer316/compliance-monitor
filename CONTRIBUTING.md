# Contributing to Compliance Monitor

Thanks for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Error messages or screenshots

### Suggesting Features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and describe:
- The problem you're trying to solve
- Your proposed solution
- Alternative approaches you've considered

### Adding New Sources

1. Edit `config/sources.yaml`
2. Add your source with name, URL, type
3. Test with `python run.py scan`
4. Submit PR with description of what the source monitors

### Code Contributions

#### Development Setup

```bash
git clone https://github.com/ganeshgunti/compliance-monitor.git
cd compliance-monitor
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python run.py init
python run.py demo
```

#### Code Style

- **Python**: Black formatting (`black .`)
- **JavaScript**: Prettier (`prettier --write dashboard/`)
- **Type hints** where applicable
- **Docstrings** for public functions
- **Comments** for complex logic

#### Pull Request Process

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request with:
   - Clear description of changes
   - Screenshots if UI changes
   - Test results

#### Testing

Before submitting PR:
- Test with demo data: `python run.py demo && python run.py list`
- Test filters in dashboard
- Check console for errors
- Verify mobile responsiveness

## Project Areas

### Easy Contributions
- Add monitoring sources to `config/sources.yaml`
- Improve documentation
- Fix typos or formatting
- Add MCC labels to dashboard

### Medium Difficulty
- Enhance dashboard UI/UX
- Add new export formats
- Improve relevance scoring algorithm
- Add email/Slack alerts

### Advanced
- Add authentication/multi-user support
- Implement scheduled scanning
- Migrate to PostgreSQL
- Add ML-based change filtering

## Questions?

Open a [Discussion](https://github.com/ganeshgunti/compliance-monitor/discussions) or ask in your PR.

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

---

**Thank you for making Compliance Monitor better!** 🚀
