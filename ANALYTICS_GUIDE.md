# Analytics Setup Guide

This guide shows you how to track GitHub repository engagement and dashboard visitors after you open source your project.

---

## Part 1: GitHub Repository Analytics

### A. Built-in GitHub Insights (Free, No Setup Required)

Once your repo is public, GitHub automatically tracks:

**How to access:**
1. Go to https://github.com/ganeshiyer316/compliance-monitor
2. Click **Insights** tab (top navigation)
3. Click **Traffic** (left sidebar)

**Available metrics:**
- 📊 **Views**: Total page views (last 14 days)
- 👥 **Unique visitors**: Individual visitors (last 14 days)
- 📥 **Clones**: Git clone operations
- 📄 **Popular content**: Most viewed files/pages
- 🔗 **Referrers**: Traffic sources (LinkedIn, Twitter, HackerNews, etc.)

**Other engagement metrics:**
- ⭐ **Stars**: Click "Stargazers" to see who starred
- 🍴 **Forks**: Click "Network → Forks" to see who forked
- 👨‍💻 **Contributors**: See all contributors
- 🔔 **Watchers**: See who's watching for updates

**LinkedIn tracking hack:**
- After posting on LinkedIn, check **Referrers** in Traffic
- You'll see `linkedin.com` as a source with visitor counts
- This shows how many clicked from your LinkedIn post

**Limitations:**
- Only last 14 days of traffic data
- No long-term historical data
- No detailed user behavior

---

### B. GitHub Badges (Added to README)

We've added these badges to your README:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/ganeshiyer316/compliance-monitor?style=social)](https://github.com/ganeshiyer316/compliance-monitor/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ganeshiyer316/compliance-monitor?style=social)](https://github.com/ganeshiyer316/compliance-monitor/network/members)
[![GitHub issues](https://img.shields.io/github/issues/ganeshiyer316/compliance-monitor)](https://github.com/ganeshiyer316/compliance-monitor/issues)
[![GitHub license](https://img.shields.io/github/license/ganeshiyer316/compliance-monitor)](https://github.com/ganeshiyer316/compliance-monitor/blob/main/LICENSE)
```

**These show:**
- Real-time star count (updates automatically)
- Fork count
- Open issues count
- License type

---

### C. Star History (Free Visualization Tool)

Track your GitHub stars over time with beautiful charts.

**Option 1: Star History Website**
- Visit: https://star-history.com/
- Enter: `ganeshiyer316/compliance-monitor`
- Get embeddable chart showing star growth

**Option 2: Add Star History Badge to README**

Add this to your README:

```markdown
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ganeshiyer316/compliance-monitor&type=Date)](https://star-history.com/#ganeshiyer316/compliance-monitor&Date)
```

This creates a chart showing your star growth over time.

---

### D. GitHub API for Custom Analytics (Advanced)

Use GitHub's API to build custom dashboards:

```bash
# Get repository stats
curl https://api.github.com/repos/ganeshiyer316/compliance-monitor

# Get stargazers with timestamps
curl https://api.github.com/repos/ganeshiyer316/compliance-monitor/stargazers

# Get forks
curl https://api.github.com/repos/ganeshiyer316/compliance-monitor/forks
```

**Useful metrics from API:**
- `stargazers_count`: Total stars
- `forks_count`: Total forks
- `watchers_count`: Total watchers
- `open_issues_count`: Open issues
- `subscribers_count`: Repository subscribers

---

## Part 2: Dashboard Visitor Analytics

Track who visits your live dashboard at https://compliance-monitor.vercel.app

---

### A. Vercel Analytics (Recommended - Easiest)

**Best for:** Quick setup, zero configuration, privacy-friendly

**Setup (takes 2 minutes):**

1. **Enable Vercel Analytics:**
   - Go to https://vercel.com/ganeshiyer316/compliance-monitor
   - Click **Analytics** tab
   - Click **Enable Analytics**
   - That's it!

2. **Add Analytics Script to Dashboard:**

   Edit `dashboard/index.html` and add before `</body>`:

   ```html
   <!-- Vercel Analytics -->
   <script>
     window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
   </script>
   <script defer src="/_vercel/insights/script.js"></script>
   ```

3. **What you get:**
   - 📊 Page views
   - 👥 Unique visitors
   - 🌍 Geographic locations (countries)
   - 📱 Device types (mobile vs desktop)
   - 🌐 Browser types
   - 📄 Top pages

**Cost:** FREE for up to 100k events/month

**View data:**
- Vercel Dashboard → Your Project → Analytics tab

---

### B. Google Analytics 4 (Most Popular)

**Best for:** Detailed analytics, custom events, long-term tracking

**Setup:**

1. **Create Google Analytics Account:**
   - Go to https://analytics.google.com/
   - Click **Start Measuring**
   - Create account: "Compliance Monitor"
   - Create property: "compliance-monitor.vercel.app"
   - Select **Web** platform
   - Copy your **Measurement ID** (looks like `G-XXXXXXXXXX`)

2. **Add to Dashboard:**

   Edit `dashboard/index.html` and add in `<head>`:

   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

   Replace `G-XXXXXXXXXX` with your actual Measurement ID.

3. **Track Custom Events (Optional):**

   Add event tracking for filters, searches, etc.:

   ```javascript
   // Track when user applies MCC filter
   document.getElementById('mccFilter').addEventListener('change', function() {
     gtag('event', 'filter_mcc', {
       'event_category': 'filter',
       'event_label': this.value
     });
   });

   // Track when user searches
   document.getElementById('searchInput').addEventListener('input', function() {
     gtag('event', 'search', {
       'event_category': 'engagement',
       'search_term': this.value
     });
   });
   ```

**What you get:**
- 📊 Real-time visitor count
- 👥 Daily/weekly/monthly active users
- 🌍 Geographic data (cities, countries)
- 📱 Device types, OS, browsers
- 📄 Page views, session duration
- 🔗 Traffic sources (LinkedIn, Twitter, HackerNews)
- 📈 Custom events (filter usage, searches)
- 🎯 Conversion funnels
- 📊 Custom dashboards

**Cost:** FREE (unlimited)

**View data:**
- https://analytics.google.com/

---

### C. Plausible Analytics (Privacy-Focused Alternative)

**Best for:** GDPR compliance, no cookies, lightweight

**Setup:**

1. **Sign up:**
   - Go to https://plausible.io/
   - Create account ($9/month or $90/year for 10k visitors/month)

2. **Add your site:**
   - Add domain: `compliance-monitor.vercel.app`
   - Copy your tracking script

3. **Add to Dashboard:**

   Edit `dashboard/index.html` and add before `</body>`:

   ```html
   <!-- Plausible Analytics -->
   <script defer data-domain="compliance-monitor.vercel.app" src="https://plausible.io/js/script.js"></script>
   ```

**What you get:**
- 📊 Page views
- 👥 Unique visitors
- 🌍 Top countries
- 🔗 Referrer sources (LinkedIn, etc.)
- 📄 Top pages
- **Privacy-friendly** (no cookies, GDPR compliant)

**Cost:** $9/month (or self-host for FREE)

---

### D. Simple Visitor Counter (Free, Self-Hosted)

**Best for:** Just want to count visitors, minimal setup

**Option 1: Simple JavaScript Counter**

Add this to `dashboard/index.html`:

```html
<script>
  // Simple visitor counter using localStorage
  (function() {
    const storageKey = 'visitor_id';
    const apiEndpoint = 'https://api.countapi.xyz/hit/compliance-monitor/visits';

    // Check if visitor has been counted
    if (!localStorage.getItem(storageKey)) {
      localStorage.setItem(storageKey, Date.now());

      // Increment counter
      fetch(apiEndpoint)
        .then(res => res.json())
        .then(data => console.log('Total visits:', data.value));
    }
  })();
</script>
```

**Option 2: Use GoatCounter (Free, Open Source)**

1. Sign up at https://www.goatcounter.com/ (FREE)
2. Add domain: `compliance-monitor`
3. Add script to dashboard:

```html
<script data-goatcounter="https://compliance-monitor.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

**Cost:** FREE

---

## Part 3: Recommended Setup

For your use case (LinkedIn post + open source), I recommend:

### Minimal Setup (5 minutes):
1. ✅ **GitHub Badges** - Already added to README
2. ✅ **GitHub Insights** - Built-in, no setup needed
3. ✅ **Vercel Analytics** - Enable in Vercel dashboard (2 minutes)

This gives you:
- GitHub: stars, forks, traffic from LinkedIn
- Dashboard: visitor counts, geographic data, referrer sources

### Complete Setup (15 minutes):
1. ✅ **GitHub Badges** - Already added
2. ✅ **GitHub Insights** - Built-in
3. ✅ **Vercel Analytics** - Quick and easy
4. ✅ **Google Analytics** - Detailed long-term tracking

This gives you everything: GitHub engagement + comprehensive dashboard analytics.

---

## Part 4: Tracking LinkedIn Impact

After you post on LinkedIn, here's how to see the impact:

### GitHub (24 hours after posting):
1. Go to https://github.com/ganeshiyer316/compliance-monitor/graphs/traffic
2. Check **Referrers** section
3. Look for `linkedin.com` - shows clicks from LinkedIn
4. Check **Views** and **Unique visitors** spike
5. Monitor **Stars** and **Forks** increase

### Dashboard (immediately):
1. **Vercel Analytics:**
   - Vercel Dashboard → Analytics → Referrers
   - Look for `linkedin.com` traffic
   - See real-time visitor count

2. **Google Analytics:**
   - GA Dashboard → Real-time
   - See live visitors browsing your dashboard
   - Check Acquisition → Traffic Sources → `linkedin.com`

### What to measure:
- 📊 **GitHub stars** (social proof)
- 👥 **GitHub visitors** (developer interest)
- 🍴 **GitHub forks** (people trying it)
- 🌐 **Dashboard visitors** (end-user interest)
- 🔗 **LinkedIn clicks** (post engagement)
- 💬 **GitHub issues** (questions/feedback)
- 👨‍💻 **Contributors** (developer collaboration)

---

## Part 5: Implementation Checklist

### Before LinkedIn Post:
- [ ] Add Vercel Analytics to dashboard
- [ ] Add Google Analytics to dashboard (optional)
- [ ] Test analytics are working (visit dashboard, check data appears)
- [ ] Create LICENSE file (needed for license badge)
- [ ] Verify all badges show correctly on README

### After LinkedIn Post:
- [ ] Check GitHub Insights → Traffic (24 hours later)
- [ ] Check Vercel Analytics dashboard
- [ ] Check Google Analytics (if enabled)
- [ ] Monitor stars/forks in real-time
- [ ] Respond to GitHub issues/discussions

---

## Part 6: Analytics Implementation (Code)

I'll add Vercel Analytics to your dashboard now. Here's what I'm adding:

**File: `dashboard/index.html`**
```html
<!-- Before closing </body> tag -->
<script>
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
</script>
<script defer src="/_vercel/insights/script.js"></script>
```

Then you just need to:
1. Enable Analytics in your Vercel dashboard
2. Deploy the updated code
3. Done!

For Google Analytics, you'll need to:
1. Get your Measurement ID
2. Add the GA script to the `<head>` section
3. Deploy

---

## Summary

**Easiest setup (5 min):**
- GitHub Insights (built-in)
- Vercel Analytics (add script + enable)

**Best setup (15 min):**
- GitHub Insights
- Vercel Analytics
- Google Analytics

**LinkedIn impact tracking:**
- GitHub Insights → Referrers
- Vercel/GA → Traffic Sources → linkedin.com
- Watch stars and forks increase

**Next steps:**
1. I'll add Vercel Analytics script to your dashboard
2. You enable it in Vercel dashboard when ready
3. Post on LinkedIn
4. Track the results!

---

**Last Updated:** January 10, 2026
