"""
Demo Data Generator - Creates realistic test data.
Useful for testing the system without making actual API calls.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from utils import db_utils

logger = logging.getLogger(__name__)


def generate_demo_data(db_path: str) -> None:
    """
    Generate demo compliance items for testing.

    Creates 5 realistic compliance items with various priorities,
    deadlines, and relevance scores.

    Args:
        db_path: Path to SQLite database
    """
    logger.info("Generating demo compliance data")

    # Demo source (will be created if doesn't exist)
    source_id = db_utils.insert_source(
        db_path,
        name="Demo Source - Payment Scheme Updates",
        url="https://example.com/demo",
        source_type="demo",
        active=True
    )

    # Create demo snapshots and changes
    demo_items = [
        {
            'title': 'Visa AFT Recipient Data Requirements',
            'summary': 'Visa is mandating new recipientDetails fields for all Account Funding Transactions (AFT). Merchants processing crypto purchases or securities trading must include enhanced recipient information including name, address, and account details. Non-compliance will result in transaction declines.',
            'deadline': (datetime.now() + timedelta(days=85)).strftime('%Y-%m-%d'),
            'impact_level': 'high',
            'mccs': json.dumps(['6051', '6211']),
            'regions': json.dumps(['Global']),
            'transaction_types': json.dumps(['AFT', 'Original Credit']),
            'technical_requirements': json.dumps([
                'Add recipientDetails object to AFT API requests',
                'Include recipientName, recipientAddress, recipientAccountNumber fields',
                'Implement validation for required fields before submission',
                'Update error handling for new decline codes',
                'Add logging for recipient data validation failures'
            ]),
            'keywords': json.dumps(['AFT', 'Visa', 'crypto', 'recipient data', 'compliance', 'API']),
            'relevance_score': 10
        },
        {
            'title': 'Mastercard Enhanced Fraud Monitoring - Q2 2026 Update',
            'summary': 'Mastercard is rolling out updated Enhanced Fraud Monitoring (EFM) rules affecting high-risk MCCs. New thresholds for fraud-to-sales ratios and chargeback monitoring. Crypto and forex merchants must maintain fraud rates below 0.5% or face program enrollment.',
            'deadline': (datetime.now() + timedelta(days=120)).strftime('%Y-%m-%d'),
            'impact_level': 'high',
            'mccs': json.dumps(['6051', '6211', '6211']),
            'regions': json.dumps(['Global']),
            'transaction_types': json.dumps(['Purchase', 'Refund']),
            'technical_requirements': json.dumps([
                'Implement real-time fraud-to-sales ratio monitoring',
                'Create automated alerts for threshold breaches',
                'Add dashboard for EFM compliance tracking',
                'Enhance transaction risk scoring algorithms',
                'Implement automated chargeback reporting'
            ]),
            'keywords': json.dumps(['EFM', 'fraud', 'Mastercard', 'chargeback', 'monitoring', 'compliance']),
            'relevance_score': 9
        },
        {
            'title': 'CBUAE VASP Guidelines - Crypto Exchange Requirements',
            'summary': 'Central Bank of UAE has issued new guidelines for Virtual Asset Service Providers (VASPs). All crypto exchanges operating in UAE must register and comply with enhanced KYC/AML requirements, transaction monitoring, and reporting obligations by June 2026.',
            'deadline': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d'),
            'impact_level': 'high',
            'mccs': json.dumps(['6051']),
            'regions': json.dumps(['MENA', 'UAE']),
            'transaction_types': json.dumps(['Crypto Purchase', 'Crypto Sale', 'Crypto Transfer']),
            'technical_requirements': json.dumps([
                'Implement enhanced KYC verification workflow',
                'Add real-time transaction monitoring for suspicious activity',
                'Create automated suspicious transaction reporting (STR) system',
                'Implement customer risk rating system',
                'Add audit trail for all compliance checks'
            ]),
            'keywords': json.dumps(['CBUAE', 'VASP', 'crypto', 'KYC', 'AML', 'UAE', 'MENA']),
            'relevance_score': 10
        },
        {
            'title': 'Visa Direct API v2.0 Migration',
            'summary': 'Visa is deprecating API v1.0 for Visa Direct disbursements. All integrations must migrate to v2.0 which includes new authentication, enhanced data fields, and improved error handling. Legacy API will be shut down September 2026.',
            'deadline': (datetime.now() + timedelta(days=240)).strftime('%Y-%m-%d'),
            'impact_level': 'medium',
            'mccs': json.dumps(['6051', '6211']),
            'regions': json.dumps(['Global']),
            'transaction_types': json.dumps(['OCT', 'Visa Direct']),
            'technical_requirements': json.dumps([
                'Update Visa Direct integration to API v2.0',
                'Implement OAuth 2.0 authentication',
                'Add new mandatory data fields to disbursement requests',
                'Update error handling for v2.0 response codes',
                'Test all disbursement flows in sandbox environment'
            ]),
            'keywords': json.dumps(['Visa Direct', 'API', 'migration', 'OCT', 'disbursement']),
            'relevance_score': 8
        },
        {
            'title': 'PCI DSS v4.0 Compliance Deadline',
            'summary': 'PCI Security Standards Council has set final deadline for PCI DSS v4.0 compliance. All merchants and service providers must complete migration from v3.2.1. Key changes include enhanced multi-factor authentication, updated encryption standards, and new security testing requirements.',
            'deadline': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
            'impact_level': 'medium',
            'mccs': json.dumps(['6051', '6211', '5999']),
            'regions': json.dumps(['Global']),
            'transaction_types': json.dumps(['All card transactions']),
            'technical_requirements': json.dumps([
                'Implement MFA for all administrative access',
                'Update encryption to TLS 1.3 minimum',
                'Conduct quarterly vulnerability scanning',
                'Implement automated security testing in CI/CD pipeline',
                'Update data retention policies and procedures'
            ]),
            'keywords': json.dumps(['PCI DSS', 'security', 'compliance', 'encryption', 'MFA']),
            'relevance_score': 7
        },
        {
            'title': 'Mastercard Gambling Merchant Monitoring Program Updates',
            'summary': 'Mastercard is implementing stricter monitoring requirements for gambling merchants (MCC 7995). New rules include enhanced fraud-to-sales ratio thresholds of 0.75%, mandatory real-time transaction monitoring, age verification requirements, and responsible gambling tools. Non-compliant merchants face potential program removal.',
            'deadline': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'impact_level': 'high',
            'mccs': json.dumps(['7995']),
            'regions': json.dumps(['Global', 'Europe', 'MENA']),
            'transaction_types': json.dumps(['Purchase', 'Refund', 'Chargeback']),
            'technical_requirements': json.dumps([
                'Implement real-time fraud-to-sales ratio monitoring (max 0.75%)',
                'Add age verification at account registration and deposit',
                'Create self-exclusion and cooling-off period functionality',
                'Implement deposit limits and loss limits',
                'Add responsible gambling messaging and tools',
                'Create automated chargeback monitoring and alerts',
                'Implement geolocation checks for restricted jurisdictions'
            ]),
            'keywords': json.dumps(['gambling', 'betting', 'casino', 'Mastercard', '7995', 'fraud monitoring', 'responsible gambling', 'age verification']),
            'relevance_score': 10
        },
        {
            'title': 'UK Gambling Commission Remote Operating License Requirements 2026',
            'summary': 'UKGC has updated remote operating license requirements for all online gambling operators. Changes include enhanced affordability checks for customers spending over £2,000/month, source of funds verification, stricter responsible gambling tools, and mandatory AI-powered player protection systems.',
            'deadline': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
            'impact_level': 'high',
            'mccs': json.dumps(['7995']),
            'regions': json.dumps(['Europe', 'UK']),
            'transaction_types': json.dumps(['Deposit', 'Withdrawal', 'Purchase']),
            'technical_requirements': json.dumps([
                'Implement affordability checks for spend over £2,000/month',
                'Add source of funds verification workflow',
                'Create AI-powered player protection and harm detection system',
                'Implement enhanced self-exclusion across all brands',
                'Add mandatory reality checks every 60 minutes',
                'Create suspicious activity reporting for money laundering',
                'Implement transaction monitoring for structuring behavior'
            ]),
            'keywords': json.dumps(['UKGC', 'gambling', 'UK', 'license', 'affordability', 'player protection', 'AML', 'responsible gambling']),
            'relevance_score': 9
        }
    ]

    # Create snapshots and compliance items
    for i, item in enumerate(demo_items, start=1):
        # Create a dummy snapshot
        content = f"Demo snapshot {i} for {item['title']}"
        content_hash = f"demo_hash_{i}_{datetime.now().timestamp()}"

        snapshot_id = db_utils.insert_snapshot(
            db_path,
            source_id,
            content,
            content_hash,
            status='success'
        )

        # Create a dummy change
        diff_text = f"+ {item['title']}\n+ New compliance requirement detected\n+ {item['summary'][:100]}..."

        change_id = db_utils.insert_change(
            db_path,
            source_id,
            None,  # No old snapshot for demo
            snapshot_id,
            diff_text
        )

        # Create compliance item
        compliance_id = db_utils.insert_compliance_item(
            db_path,
            change_id,
            source_id,
            item
        )

        # Mark change as analyzed
        db_utils.mark_change_analyzed(db_path, change_id)

        logger.info(f"Created demo item {i}: {item['title']}")

    logger.info(f"Successfully generated {len(demo_items)} demo compliance items")
    print(f"\n[OK] Generated {len(demo_items)} demo compliance items")
    print("  Run 'python run.py list' to view them")
