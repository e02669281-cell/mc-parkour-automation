# MC Parkour Automation

**Fully automated Minecraft parkour video generation, vault management, and multi-account posting system for TikTok and YouTube Shorts**

## Overview

This system handles the complete workflow for posting 3+ videos daily to 3-5 TikTok accounts and 3-5 YouTube channels with minimal manual intervention. It includes:

- **Vault Management**: Automatic video ingestion, deduplication, and organization
- **Smart Rotation**: Prevents same video on same account within 7-day cooldown
- **Multi-Account Scheduling**: Per-account schedules with customizable posting times
- **Caption Rotation**: Different hooks per account to prevent "obvious duplicates"
- **Windows Task Automation**: Cron-like scheduling via Task Scheduler

## Quick Start

### 1. Create Folder Structure

```bash
D:\mc_parkour_factory\
├── incoming\           # Drop Revid clips here
├── vault\             # Organized by date
├── scheduled\         # Upload schedules (auto-generated)
├── config\            # accounts.json, settings.json
├── captions\          # hooks_tiktok.json, hooks_youtube.json
├── scripts\           # Python utilities
└── logs\              # vault.csv tracking
```

### 2. Configure Your Accounts

Edit `config/accounts.json` with your TikTok and YouTube account details:

```json
{
  "tiktok_accounts": [
    {
      "account_id": 1,
      "username": "your_tiktok_1",
      "email": "email@example.com",
      "posts_per_day": 3,
      "posting_times": ["10:00", "14:30", "19:45"],
      "reuse_cooldown_days": 7,
      "hook_profile": "aggressive"
    }
  ]
}
```

### 3. Daily Workflow

**Step 1: Generate clips in Revid**
- Create 30-60 vertical parkour shorts (9:16 aspect ratio)
- Export to `incoming/` folder

**Step 2: Run vault manager**
```bash
python scripts/vault_manager.py
```
- Moves clips to vault
- Prevents duplicate uploads
- Updates `logs/vault.csv`

**Step 3: Generate upload schedules**
```bash
python scripts/upload_scheduler.py
```
- Creates per-account CSV files in `scheduled/`
- Ensures 3+ posts/day per account
- Respects 7-day reuse cooldown

**Step 4: Post to TikTok/YouTube**
- Use TikTok uploader tool with generated CSVs
- Use YouTube Studio scheduler for Shorts

## File Structure

| File | Purpose |
|------|----------|
| `SETUP_GUIDE.md` | Detailed setup and architecture |
| `config/accounts.json` | Account credentials and posting times |
| `config/settings.json` | Global configuration |
| `captions/hooks_tiktok.json` | TikTok caption variations by profile |
| `captions/hooks_youtube.json` | YouTube caption variations by profile |
| `scripts/vault_manager.py` | Ingests and deduplicates videos |
| `scripts/upload_scheduler.py` | Generates per-account upload schedules |
| `logs/vault.csv` | Master record of all videos |

## Automation Phases

### Phase 1: Semi-Manual (Current)
- You generate clips in Revid
- Run Python scripts to organize & schedule
- Manually post or use uploader tools

### Phase 2: Partial Automation
- Windows Task Scheduler runs scripts daily
- Browser automation uploads to accounts

### Phase 3: Full Automation
- Script generates video ideas from trends
- Headless Revid API generates clips
- Scheduled posting to all accounts via APIs

## Key Features

✅ **De-duplication**: MD5 hashing prevents exact duplicate uploads  
✅ **Reuse Prevention**: 7-day cooldown per account (customizable)  
✅ **Caption Variety**: Different hooks per account prevent "obvious duplicates"  
✅ **Vault Tracking**: CSV logging of all videos and usage  
✅ **Scalable**: Easily add more accounts or adjust posting frequency  
✅ **Modular**: Each script can run independently  

## Requirements

- Python 3.8+
- Windows (for Task Scheduler automation)
- Revid (for clip generation)
- TikTok account(s) + YouTube channel(s)
- TikTok uploader tool (e.g., TikTokAutoUploader)

## Configuration

All settings are in `config/settings.json`:

```json
{
  "base_path": "D:\\mc_parkour_factory",
  "min_vault_days": 7,
  "min_videos_per_day_needed": 45,
  "randomize_posting_times": true,
  "time_variance_minutes": 20
}
```

## Troubleshooting

**Q: Vault is running out of videos**  
A: Increase Revid generation frequency or reduce posts/day per account

**Q: Same video appearing on same account within 7 days**  
A: Check `logs/vault.csv` and verify cooldown enforcement in scripts

**Q: Uploads failing**  
A: Check account quotas, API limits, and uploader tool logs

## License

MIT License - Feel free to modify and use as needed

## Next Steps

1. Clone this repo and follow SETUP_GUIDE.md
2. Generate first batch of videos in Revid
3. Test vault_manager.py and upload_scheduler.py
4. Manually post to verify everything works
5. Gradually automate with cron/Task Scheduler + uploader tools
