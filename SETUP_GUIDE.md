# MC Parkour Automation - Complete Setup Guide

## Overview

This is a fully automated system for generating, managing, and posting Minecraft parkour videos across 3-5 TikTok and 3-5 YouTube accounts with at least 3 posts per account daily.

**Features:**
- Automatic video vault management with de-duplication
- Multi-account scheduling and rotation
- Smart re-use prevention (7-day cooldown per account)
- Caption hook rotation for content variation
- Windows Task Scheduler automation (Phase 1+)

---

## Directory Structure

```
mc_parkour_factory/
├── incoming/                    # Drop raw Revid clips here
├── vault/
│   └── YYYY-MM-DD/
│       ├── raw/                 # Organized video files
│       └── scheduled/           # Tracking files
├── scheduled/
│   ├── tiktok/                  # Per-account schedules
│   └── youtube/                 # Per-channel schedules
├── config/
│   ├── accounts.json            # Account configurations
│   └── settings.json            # Global settings
├── captions/
│   ├── hooks_tiktok.json       # TikTok captions by profile
│   ├── hooks_youtube.json      # YouTube captions by profile
│   └── caption_templates.json  # Caption formats
├── scripts/
│   ├── vault_manager.py        # Core vault logic
│   ├── upload_scheduler.py     # Generate upload plans
│   └── caption_rotator.py      # Hook selection
└── logs/
    ├── vault.csv               # Master file tracking
    └── upload_log.csv          # Upload history
```

---

## Phase 1: Manual Setup (Current)

### Step 1: Create Folder Structure

Create the folder structure above on your Windows PC. Recommended base path: `D:\mc_parkour_factory`

### Step 2: Configure Accounts

Create `config/accounts.json`:

```json
{
  "tiktok_accounts": [
    {
      "account_id": 1,
      "username": "your_tiktok_1",
      "email": "email1@example.com",
      "posts_per_day": 3,
      "posting_times": ["10:00", "14:30", "19:45"],
      "reuse_cooldown_days": 7,
      "hook_profile": "aggressive"
    }
  ],
  "youtube_accounts": [
    {
      "channel_id": 1,
      "channel_name": "MC Parkour - Channel 1",
      "email": "yt_email1@example.com",
      "posts_per_day": 3,
      "posting_times": ["11:00", "15:00", "20:00"],
      "reuse_cooldown_days": 7,
      "hook_profile": "educational"
    }
  ]
}
```

### Step 3: Run Daily Workflow

**Daily routine:**

1. **Generate clips in Revid:**
   - Create 30-60 Minecraft parkour shorts (vertical 9:16)
   - Export to `incoming/` folder
   - Suggested frequency: Once daily or every 2-3 days

2. **Run vault manager:**
   ```bash
   python scripts/vault_manager.py
   ```
   - Moves clips from `incoming/` to vault
   - Tracks files in `logs/vault.csv`
   - Prevents re-uploads of exact duplicates

3. **Generate upload schedules:**
   ```bash
   python scripts/upload_scheduler.py
   ```
   - Creates per-account schedule CSVs in `scheduled/`
   - Rotates videos across accounts
   - Applies 7-day reuse cooldown per account
   - Prevents same video on same account within cooldown

4. **Post to TikTok (manual or automated):**
   - Use TikTok MultiAccountUploader or similar tool
   - Load `scheduled/tiktok/account_*_schedule.csv`
   - Post at scheduled times

5. **Post to YouTube (manual or automated):**
   - Log into YouTube Studio for each channel
   - Use scheduler feature (Shorts uploads)
   - Or use YouTube uploader tool with CSV input

---

## Phase 2: Partial Automation

Once Phase 1 works smoothly:

1. **Windows Task Scheduler:**
   ```
   Task: "MC Parkour - Daily Vault Update"
   Trigger: Daily at 6:00 AM
   Action: Run `python scripts/vault_manager.py` + `upload_scheduler.py`
   ```

2. **Browser automation (TikTok/YouTube):**
   - Use Selenium or Puppeteer to auto-login and schedule posts
   - Or integrate existing API-based uploaders

---

## Phase 3: Full Automation

- Script pulls trending topics from Reddit/Twitter
- Auto-generates scripts via LLM
- Headless Revid API integration for clip generation
- Full automated posting via APIs
- Cron jobs handle everything daily

---

## Key Files Explained

### `vault_manager.py`
- Scans `incoming/` for new videos
- Computes MD5 hash for de-duplication
- Moves files to dated vault folder
- Updates `vault.csv` with metadata
- Prevents exact duplicates

### `upload_scheduler.py`
- Reads `accounts.json` and `vault.csv`
- Builds rotation plan ensuring:
  - Each account gets 3+ posts/day
  - No video repeated on same account within 7 days
  - Videos spread across posting times
- Outputs per-account `schedule.csv` files

### `caption_rotator.py`
- Selects hook/caption based on account profile
- Allows same video file with different captions per account
- Prevents "obvious duplicate" feel

---

## Tools & Dependencies

**Python:** 3.8+
```bash
pip install python-dotenv requests
```

**TikTok Upload:**
- TikTokAutoUploader (supports multi-account)
- Or custom Selenium script

**YouTube Upload:**
- YouTube Studio (manual scheduling)
- Or yt-dlp / google-api-client for automation

---

## Important Notes

⚠️ **Account Safety:**
- Never hardcode passwords in scripts
- Use environment variables or secrets managers
- Test on 1 account before scaling to 5+

⚠️ **Content Quality:**
- Maintain consistent voice profiles across brand
- Monitor upload success rates (aim for 95%+)
- Track analytics to see which hooks perform best

⚠️ **Platform Rules:**
- TikTok: 10-60 minute uploads per account per day (varies)
- YouTube: Shorts can post multiple per day
- Both: Avoid posting exact same content too frequently

---

## Troubleshooting

**Q: Vault is running out of videos**
- A: Increase Revid generation frequency or reduce posts/day

**Q: Same video appearing on same account within 7 days**
- A: Check `vault.csv` - reuse_cooldown_days may not be enforced. Verify script logic.

**Q: Uploads failing**
- A: Check account quotas, API limits, and browser automation logs.

---

## Next Steps

1. Copy this repo locally
2. Create folder structure
3. Add config files with your accounts
4. Generate first batch of videos in Revid
5. Test `vault_manager.py` and `upload_scheduler.py`
6. Manually post first batch to verify
7. Iterate on timing and hook profiles
8. Gradually automate with cron + uploader tools
