# How to Manually Add/Update Compliance Data

## Where to Add Manual Data

**File:** `data/manual_overrides.json`

This is the **ONLY** place you should manually add or update compliance deadlines. Why?

✅ **Hard-locked** - Cannot be overwritten by automated scrapers
✅ **100% credibility** - You control the data, perfect for verified deadlines
✅ **Conflict resolution** - Automatically wins over automated items
✅ **Version control** - Easy to track changes in Git

---

## Step-by-Step: Adding a New Compliance Item

### 1. Open the File

Navigate to: `data/manual_overrides.json`

### 2. Copy This Template

```json
{
  "id": "unique-identifier-here",
  "title": "Your Compliance Requirement Title",
  "deadline": "2026-06-30",
  "mccs": ["7995", "6051", "6211"],
  "regions": ["UAE", "UK", "Europe"],
  "transaction_types": ["AFT", "OCT"],
  "impact_level": "high",
  "hard_lock": true,
  "source_name": "Visa / Mastercard / CBUAE / etc.",
  "source_url": "https://link-to-official-source.com",
  "summary": "Detailed description of what this compliance requirement means, who it affects, and what needs to be done.",
  "technical_requirements": [
    "First technical requirement or implementation step",
    "Second requirement",
    "Third requirement"
  ],
  "keywords": ["keyword1", "keyword2", "relevant-terms"],
  "relevance_score": 9,
  "notes": "Internal notes about where you verified this deadline, why it matters, etc.",
  "type": "scheme_mandate"
}
```

### 3. Fill in the Fields

#### **Required Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier (lowercase, hyphens) | `"visa-aft-uae-2026"` |
| `title` | Short, descriptive title | `"Visa AFT Mandate for UAE Merchants"` |
| `deadline` | ISO date format (YYYY-MM-DD) | `"2026-03-31"` |
| `mccs` | Array of MCC codes (strings) | `["7995", "6051", "6211"]` |
| `regions` | Array of affected regions | `["UAE", "MENA", "Global"]` |
| `impact_level` | Priority level | `"high"` / `"medium"` / `"low"` |
| `hard_lock` | Always `true` for manual items | `true` |
| `source_name` | Authority/organization | `"Visa"` / `"CBUAE"` / `"Mastercard"` |
| `summary` | What this requirement means | See example below |

#### **MVP MCC Codes (Use Only These):**

```json
"mccs": ["7995"]        // Gambling only
"mccs": ["6051"]        // Crypto only
"mccs": ["6211"]        // Securities/Brokerage only
"mccs": ["7995", "6051"] // Gambling + Crypto
"mccs": ["7995", "6051", "6211"] // All MVP categories
```

**Important:** Only items with at least ONE of these MCCs will show on the dashboard:
- **7995** - Gambling/Betting/Casino
- **6051** - Crypto/Digital Currency
- **6211** - Securities/Brokerage

#### **Optional but Recommended:**

| Field | Description | Example |
|-------|-------------|---------|
| `transaction_types` | Types of transactions affected | `["AFT", "OCT", "Recurring"]` |
| `technical_requirements` | Implementation steps | `["Implement AFT API", "Update KYC"]` |
| `keywords` | Search terms | `["aft", "mandate", "deadline"]` |
| `relevance_score` | 1-10 score | `9` |
| `notes` | Your verification notes | `"Confirmed with Visa rep on Jan 5"` |
| `type` | Classification | `"scheme_mandate"` / `"regulatory"` |

---

## Example: Real Compliance Item

```json
{
  "id": "cbuae-vasp-licensing-2026",
  "title": "CBUAE Virtual Asset Service Provider (VASP) Licensing Deadline",
  "deadline": "2026-12-31",
  "mccs": ["6051"],
  "regions": ["UAE"],
  "transaction_types": ["Crypto"],
  "impact_level": "high",
  "hard_lock": true,
  "source_name": "Central Bank of UAE",
  "source_url": "https://www.centralbank.ae/en/regulations",
  "summary": "All Virtual Asset Service Providers (VASPs) operating in the UAE must obtain CBUAE licensing by December 31, 2026. This includes crypto exchanges, wallet providers, and payment processors handling digital currencies. Failure to obtain license will result in operational shutdown.",
  "technical_requirements": [
    "Submit full licensing application to CBUAE",
    "Demonstrate AED 10M minimum capital requirement",
    "Implement comprehensive AML/CFT systems",
    "Establish local UAE headquarters with governance",
    "Pass CBUAE operational and security audit"
  ],
  "keywords": ["VASP", "crypto", "licensing", "UAE", "CBUAE", "virtual-assets"],
  "relevance_score": 10,
  "notes": "Confirmed from CBUAE Circular 21/2024. Critical deadline for UAE crypto operations.",
  "type": "regulatory"
}
```

---

## How to Add It to Your File

### 1. Open `data/manual_overrides.json`

### 2. Find the `manual_compliance_items` array

You'll see:
```json
{
  "manual_compliance_items": [
    {
      "id": "visa-aft-mandate-mena",
      ...
    },
    {
      "id": "cbuae-otp-biometric",
      ...
    }
  ]
}
```

### 3. Add a comma after the last item, then paste your new item

```json
{
  "manual_compliance_items": [
    {
      "id": "visa-aft-mandate-mena",
      ...
    },
    {
      "id": "cbuae-otp-biometric",
      ...
    },
    {
      "id": "YOUR-NEW-ITEM-ID",
      "title": "Your New Compliance Item",
      ...
    }
  ]
}
```

### 4. Save the file

### 5. Regenerate the dashboard

```bash
python run.py dashboard
```

---

## Editing Existing Items

### To Update a Deadline:

1. Find the item by its `id` in `data/manual_overrides.json`
2. Change the `deadline` field:
```json
"deadline": "2026-03-31"  // Change this
```
3. Update `notes` to track the change:
```json
"notes": "Deadline extended from Feb 28 to Mar 31 per Visa announcement"
```
4. Save and regenerate dashboard: `python run.py dashboard`

### To Update MCCs:

```json
"mccs": ["7995", "6051"]  // Add or remove MCC codes
```

**Remember:** Only MCCs **7995**, **6051**, and **6211** will show on the MVP dashboard!

### To Mark as Resolved:

Instead of deleting (lose historical data), set the deadline to past:

```json
"deadline": "2025-12-31"  // Already passed, will be archived
```

The dashboard automatically filters out past deadlines.

---

## Common Mistakes to Avoid

### ❌ **Wrong MCC Format**
```json
"mccs": [7995, 6051]  // WRONG - numbers
```

✅ **Correct:**
```json
"mccs": ["7995", "6051"]  // Strings!
```

### ❌ **Invalid Date Format**
```json
"deadline": "March 31, 2026"  // WRONG
```

✅ **Correct:**
```json
"deadline": "2026-03-31"  // ISO format (YYYY-MM-DD)
```

### ❌ **Missing Comma**
```json
{
  "id": "item-1",
  ...
}
{  // WRONG - missing comma above
  "id": "item-2",
  ...
}
```

✅ **Correct:**
```json
{
  "id": "item-1",
  ...
},  // Comma here!
{
  "id": "item-2",
  ...
}
```

### ❌ **Forgetting to Regenerate Dashboard**

After editing `manual_overrides.json`, always run:
```bash
python run.py dashboard
```

Otherwise, the changes won't appear!

---

## What Happens After You Add Data?

### 1. Run Dashboard Command
```bash
python run.py dashboard
```

### 2. You'll See Output Like:
```
Generating dashboard (Hybrid Model)...

[Layer 1] Loaded 9 hard-locked manual items  ← Your new item is here!
[Layer 2] Loaded 6 automated items

[OK] Hybrid merge complete:
  - Manual (hard-locked): 9
  - Automated (after deduplication): 6
  - Conflicts resolved: 0
  - Total items: 15
```

### 3. Dashboard Updates

Open `dashboard/index.html` in your browser and you'll see your new item!

---

## FAQ

### Q: Can I edit items that were scraped automatically?

**A:** No. Automated items are in the database (`data/compliance.db`), not in `manual_overrides.json`.

**To override an automated item:**
1. Copy its data
2. Create a new manual entry in `manual_overrides.json` with the same title/deadline/region
3. The system will automatically detect the conflict and use YOUR manual version instead

### Q: What if I want to remove an item?

**Best Practice:** Don't delete! Instead, set the deadline to a past date:

```json
"deadline": "2025-01-01"  // Will be automatically archived
```

This preserves historical data for auditing.

### Q: Can I use MCCs other than 7995, 6051, 6211?

**A:** Yes, you can add them, but they **won't show on the MVP dashboard**. The dashboard is configured to only show:
- **7995** - Gambling
- **6051** - Crypto
- **6211** - Securities/Brokerage

If you need other MCCs, ask me to update the MVP filter.

### Q: How do I verify my JSON is valid?

**Before saving:**
1. Copy your entire `manual_overrides.json` content
2. Go to https://jsonlint.com/
3. Paste and click "Validate JSON"
4. Fix any errors before saving

### Q: Where should I NOT add manual data?

**DON'T edit these:**
- ❌ `data/compliance.db` - Database (automated items only)
- ❌ `dashboard/data.json` - Generated file (gets overwritten)
- ❌ `config/sources.json` - Automated scraping sources

**ONLY edit:**
- ✅ `data/manual_overrides.json` - Your manual compliance items

---

## Quick Reference: Compliance Types

Use for the `type` field:

| Type | When to Use | Example |
|------|-------------|---------|
| `scheme_mandate` | Visa/Mastercard requirements | AFT mandate, 3DS2, tokenization |
| `regulatory` | Government/regulator rules | CBUAE licensing, VARA registration |
| `processor_change` | PSP-specific changes | Stripe API deprecation, Checkout.com fee update |

---

## Need Help?

If you're unsure about:
- What MCCs to use
- How to classify a compliance item
- Date formatting
- JSON syntax

Just ask! I can help you add the item correctly.

---

**Current Status:**
- ✅ Dashboard shows **11 items** (5 manual + 6 automated)
- ✅ MVP filter active: Only Gambling (7995), Crypto (6051), Securities (6211)
- ✅ 3 items excluded (non-MVP MCCs)

**Last Updated:** January 8, 2026
