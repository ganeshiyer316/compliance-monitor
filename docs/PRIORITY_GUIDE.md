# Priority Categorization Guide

## How Priority Levels Work

The compliance monitor uses a 3-tier priority system to help you focus on the most critical compliance requirements first.

---

## Priority Levels Explained

### 🔴 HIGH Priority

**When to use:** Critical compliance requirements with severe consequences for non-compliance.

**Characteristics:**
- **Mandatory** regulatory or scheme requirements
- **Hard deadlines** with no extensions
- **Severe penalties** for non-compliance (fines, license suspension, operational shutdown)
- **Legal obligations** (federal laws, card scheme mandates, regulator orders)
- **Business-critical** impact (can't operate without compliance)

**Examples from your data:**
- ✅ **Visa AFT Recipient Data Requirements** (Mar 31, 2026)
  - Mandatory for crypto/securities AFT transactions
  - Missing fields = transaction declines + compliance assessments

- ✅ **US GENIUS Act - Stablecoin Regulations** (Jul 18, 2026)
  - Federal licensing requirement
  - Unlicensed issuers cannot operate in US

- ✅ **UAE CBUAE Virtual Asset Licensing** (Sep 16, 2026)
  - Criminal penalties: imprisonment + fines AED 50K-500M
  - Admin fines up to AED 1B

- ✅ **UK Gambling Commission - Bonus Wagering** (Jan 19, 2026)
  - Fines up to £20M for non-compliance
  - License review/suspension risk

**Impact if ignored:**
- ❌ Fines (often millions)
- ❌ License suspension or revocation
- ❌ Criminal penalties (in some jurisdictions)
- ❌ Operational shutdown
- ❌ Transaction processing blocked

---

### ⚠️ MEDIUM Priority

**When to use:** Important requirements with moderate consequences or more flexible timelines.

**Characteristics:**
- **Important but not critical** for immediate operations
- **Flexible deadlines** or longer implementation windows
- **Moderate penalties** (smaller fines, warnings before enforcement)
- **Best practices** or industry standards (not hard legal requirements)
- **Pilot programs** or voluntary initiatives

**Examples from your data:**
- ✅ **UK Gambling Commission - Financial Key Event Reporting** (Mar 19, 2026)
  - Important for transparency, but less immediate operational impact
  - Reporting requirement, not transactional blocker

- ✅ **UK Gambling Commission - RTS 12B** (Jun 30, 2026)
  - Required for remote platforms
  - Affects player protection, not immediate business continuity

- ✅ **CFTC Blockchain Technology Rules** (Aug 31, 2026)
  - Regulatory clarity (enabling), not prohibition
  - Benefits: tokenized collateral in derivatives

- ✅ **Federal Reserve Skinny Master Account** (Dec 31, 2026)
  - Optional program for crypto firms
  - Enables direct Fed access, not mandatory

**Impact if ignored:**
- ⚠️ Smaller fines or warnings
- ⚠️ Reduced operational efficiency
- ⚠️ Competitive disadvantage
- ⚠️ Customer experience issues
- ⚠️ Audit findings (but not shutdown)

---

### 📘 LOW Priority

**When to use:** Nice-to-have initiatives, pilot programs, or future-looking requirements.

**Characteristics:**
- **Pilot programs** with limited scope
- **No immediate penalties** for non-participation
- **Long-term strategic** initiatives
- **Emerging trends** (not yet mandatory)
- **Optional programs** or voluntary participation

**Examples from your data:**
- ✅ **DTC Tokenization Pilot Launch** (Jun 30, 2026)
  - 3-year pilot only, limited scope
  - SEC no-action letter = regulatory sandbox
  - Watch for broader implications, but no immediate action required

**Impact if ignored:**
- 📌 Miss early-mover advantage
- 📌 Less regulatory clarity for future planning
- 📌 No immediate business impact

---

## How Priority is Determined

When adding manual compliance items, consider these factors:

### 1. **Legal Obligation**
- **Federal/State Law** → HIGH
- **Card Scheme Mandate** (Visa/Mastercard) → HIGH
- **Regulator Order** (FCA, CBUAE, SEC) → HIGH
- **Industry Guidance** → MEDIUM
- **Pilot Program** → LOW

### 2. **Consequence Severity**
- **License revocation / Operational shutdown** → HIGH
- **Criminal penalties / Imprisonment** → HIGH
- **Fines >$1M or >£1M** → HIGH
- **Fines <$1M** → MEDIUM
- **Warnings / Audit findings** → MEDIUM
- **No penalties (voluntary)** → LOW

### 3. **Business Impact**
- **Can't process transactions** → HIGH
- **Transaction declines / failures** → HIGH
- **Customer experience degradation** → MEDIUM
- **Reporting/disclosure only** → MEDIUM
- **Strategic advantage (optional)** → LOW

### 4. **Deadline Flexibility**
- **Hard deadline, no extensions** → HIGH
- **Possible extensions / grace periods** → MEDIUM
- **Pilot / phased rollout** → LOW

### 5. **Geographic Scope**
- **Your primary markets** → Higher priority
- **Secondary markets** → Medium priority
- **Markets you don't operate in** → Lower priority

---

## Priority Matrix

Use this quick reference:

| Consequence | Mandatory | Timeline | Priority |
|-------------|-----------|----------|----------|
| Shutdown / License loss | Yes | <90 days | **HIGH** |
| Large fines (>$1M) | Yes | <180 days | **HIGH** |
| Transaction blocking | Yes | Any | **HIGH** |
| Criminal penalties | Yes | Any | **HIGH** |
| Moderate fines (<$1M) | Yes | >180 days | **MEDIUM** |
| Reporting requirements | Yes | Any | **MEDIUM** |
| Best practices | No | Any | **MEDIUM** |
| Pilot programs | No | Any | **LOW** |
| Voluntary initiatives | No | Any | **LOW** |

---

## Your Current Dashboard Breakdown

**Total: 24 items**

### By Priority:
- **HIGH:** ~18 items (75%)
  - Most items are mandatory regulatory/scheme requirements
  - Severe consequences for non-compliance

- **MEDIUM:** ~5 items (21%)
  - Important but flexible requirements
  - Moderate penalties or longer timelines

- **LOW:** ~1 item (4%)
  - DTC Tokenization Pilot (optional)

### Why Most Items Are HIGH:

Your curated data focuses on:
1. **Federal regulations** (US GENIUS Act, California DFAL) → HIGH
2. **Card scheme mandates** (Visa AFT requirements) → HIGH
3. **UAE/UK regulator orders** (CBUAE licensing, UKGC rules) → HIGH
4. **Global tax reporting** (OECD CARF) → HIGH

These are all **mandatory** with **severe penalties**, so HIGH priority is appropriate.

---

## How to Set Priority When Adding Data

When editing `data/manual_overrides.json`:

```json
"impact_level": "high"  // or "medium" or "low"
```

**Decision Tree:**

1. **Is it mandatory by law/regulation?**
   - Yes → Check consequences
   - No → Probably MEDIUM or LOW

2. **What happens if you don't comply?**
   - License loss / shutdown → **HIGH**
   - Fines >$1M or criminal → **HIGH**
   - Fines <$1M → **MEDIUM**
   - Warnings / audit findings → **MEDIUM**
   - Nothing (voluntary) → **LOW**

3. **Does it block transactions?**
   - Yes → **HIGH**
   - No → Check other factors

4. **What's the deadline?**
   - <90 days + mandatory → **HIGH**
   - >180 days + moderate penalties → **MEDIUM**
   - Pilot/no deadline → **LOW**

---

## Visual Indicators on Dashboard

The dashboard uses color coding:

- 🔴 **HIGH** = Red border + "HIGH" badge
- ⚠️ **MEDIUM** = Orange border + "MEDIUM" badge
- 📘 **LOW** = Green border + "LOW" badge

Plus urgency indicators based on deadline:
- 🚨 **OVERDUE** (past deadline) - pulsing red
- 🔴 **URGENT** (≤30 days) - red
- ⚠️ **SOON** (31-90 days) - orange
- 📅 **Upcoming** (91-180 days) - blue

---

## Recommendations for Your Use Case

Given your focus on **Gambling (7995), Crypto (6051), and Securities (6211)**:

### Most Critical (HIGH):
1. **Visa AFT Requirements** - Transaction blocking risk
2. **US Stablecoin Regulations** - License requirement
3. **UAE CBUAE Licensing** - Criminal penalties
4. **UK Gambling Rules** - £20M fines + license loss
5. **EU/UK Crypto Travel Rule** - Every transaction affected
6. **OECD CARF Tax Reporting** - Global tax compliance

### Important But Flexible (MEDIUM):
1. **CFTC Blockchain Rules** - Enabling regulation
2. **Fed Master Accounts** - Optional program
3. **UK Gambling Reporting** - Transparency requirement

### Watch But Not Urgent (LOW):
1. **DTC Tokenization Pilot** - 3-year pilot, limited scope

---

## When to Escalate Priority

You might need to **upgrade** an item from MEDIUM → HIGH if:

- ✅ Your company operates in that jurisdiction and timeline is approaching
- ✅ Regulator issues enforcement action or warning letter
- ✅ Competitors receive penalties for non-compliance
- ✅ You receive direct communication from regulator
- ✅ Deadline gets moved up

---

## FAQ

**Q: Should I set everything to HIGH to be safe?**
**A:** No. If everything is HIGH, nothing is truly prioritized. Use HIGH only for mandatory requirements with severe consequences. This helps your team focus on what truly matters.

**Q: What if I'm not sure between HIGH and MEDIUM?**
**A:** Ask: "If we miss this deadline, what happens?" If the answer is "fines >$1M, license loss, or can't process transactions" → HIGH. If it's "warnings, audit findings, or smaller fines" → MEDIUM.

**Q: Can priority change over time?**
**A:** Yes! As deadlines approach, or if enforcement increases, you can update the `impact_level` field in `manual_overrides.json` and regenerate the dashboard.

**Q: Do automated items have priorities?**
**A:** Yes, the intelligence agent assigns priorities based on keywords and content analysis. Manual items override these.

---

## Summary

**Priority is based on:**
1. Legal obligation (mandatory vs. voluntary)
2. Consequence severity (shutdown vs. warnings)
3. Business impact (transaction blocking vs. reporting)
4. Deadline urgency (imminent vs. flexible)

**Your current distribution (75% HIGH) is appropriate** because you're tracking:
- Federal laws with criminal penalties
- Card scheme mandates that block transactions
- Regulator orders with license-loss risk

**Action:** Review your 24 items and confirm the priority levels match your business risk tolerance. Update `impact_level` in `manual_overrides.json` if needed.

---

**Last Updated:** January 8, 2026
