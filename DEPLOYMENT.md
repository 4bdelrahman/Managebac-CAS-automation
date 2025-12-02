# GitHub Actions Deployment Guide

Complete setup guide for deploying your CAS automation to GitHub Actions for daily cloud execution.

---

## 📋 Prerequisites

Before deploying, ensure you have:
- [x] A GitHub account
- [x] Your ManageBac credentials
- [x] A Gemini API key
- [x] This repository pushed to GitHub

---

## 🚀 Step-by-Step Deployment

### 1. Push Your Code to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CAS automation setup"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/managebac.git
git branch -M main
git push -u origin main
```

---

### 2. Configure GitHub Secrets

GitHub Secrets keep your credentials secure. Never commit passwords to your repository!

**Steps:**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each of the following secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `GEMINI_API_KEY` | Your Gemini API key | `AIza...` |
| `MANAGEBAC_URL` | Your school's ManageBac URL | `https://yourschool.managebac.com` |
| `MANAGEBAC_USERNAME` | Your ManageBac username/email | `student@school.com` |
| `MANAGEBAC_PASSWORD` | Your ManageBac password | `YourPassword123` |

> [!IMPORTANT]
> **Double-check your credentials!** Wrong credentials will cause the workflow to fail silently.

---

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

---

### 4. Test the Workflow Manually

Before relying on the schedule, test manually:

1. Go to **Actions** tab
2. Select **CAS Autopilot** workflow (left sidebar)
3. Click **Run workflow** dropdown (right side)
4. Click the green **Run workflow** button
5. Wait 2-3 minutes and refresh the page
6. Click on the running workflow to see live logs

**What should happen:**
- ✅ Dependencies install
- ✅ Playwright browsers install
- ✅ Smart scheduler checks if run is due
- ✅ If due: generates idea → reflection → submits to ManageBac
- ✅ If not due: skips and exits

---

### 5. Verify the Submission

After a successful run:

1. **Check the logs**: Look for ✅ success messages
2. **Download artifacts**:
   - Scroll to bottom of workflow run page
   - Download `cas-automation-output.zip`
   - Contains: generated idea, reflection, screenshot
3. **Verify on ManageBac**: Log in and check your CAS reflections

---

## ⏰ Schedule Configuration

The workflow runs **daily at 10:00 UTC** (12:00 PM Egypt time).

The smart scheduler (`run_if_due.py`) checks if 4 days have passed since the last run. If not, it skips execution.

### Change the Schedule

Edit [`.github/workflows/cas_scheduler.yml`](file:///d:/Coding/managebac/.github/workflows/cas_scheduler.yml):

```yaml
on:
  schedule:
    # Run daily at 10:00 UTC
    - cron: '0 10 * * *'
```

**Cron format:** `minute hour day month weekday`

Examples:
- `0 10 * * *` - Daily at 10:00 UTC
- `0 */6 * * *` - Every 6 hours
- `0 10 * * 1` - Every Monday at 10:00 UTC

> [!TIP]
> Use [crontab.guru](https://crontab.guru/) to test cron expressions

---

## 🔍 Monitoring & Debugging

### View Workflow Runs

1. Go to **Actions** tab
2. Click on any workflow run to see details
3. Click on job name to see step-by-step logs

### Email Notifications

GitHub automatically emails you when workflows fail. To customize:

1. Click your profile → **Settings** (not repository settings!)
2. Go to **Notifications**
3. Under "Actions", configure failure alerts

### Download Debug Artifacts

When workflows run, they save useful files:

**On every run** (`cas-automation-output`):
- `generated_idea.json` - The AI-generated activity
- `generated_reflection.json` - The full reflection text
- `submission_screenshot.png` - Screenshot after submission
- `last_run.json` - Timestamp tracking

**On failure** (`playwright-traces`):
- Full `.tmp/` directory for debugging

### Common Issues

| Problem | Solution |
|---------|----------|
| **Login failed** | Check `MANAGEBAC_USERNAME` and `MANAGEBAC_PASSWORD` secrets |
| **API error** | Verify `GEMINI_API_KEY` is correct and has quota |
| **Workflow skipped** | Smart scheduler determined it's not due yet (check `last_run.json`) |
| **Playwright timeout** | ManageBac UI may have changed - update selectors in `submit_to_managebac.py` |

---

## 🛠 Advanced Configuration

### Run Every 4 Days Instead of Daily

If you want to rely on cron instead of the smart scheduler:

```yaml
on:
  schedule:
    - cron: '0 10 */4 * *'  # Every 4 days
```

Then modify the workflow to call scripts directly:

```yaml
run: |
  python execution/generate_idea.py
  python execution/generate_reflection.py --auto
  python execution/submit_to_managebac.py --auto
```

### Add Slack/Discord Notifications

Use GitHub Actions integrations to send notifications on success/failure.

Example (add after the run step):

```yaml
- name: Notify on Discord
  if: success()
  run: |
    curl -X POST -H 'Content-Type: application/json' \
    -d '{"content":"✅ CAS reflection submitted!"}' \
    ${{ secrets.DISCORD_WEBHOOK_URL }}
```

---

## 📊 Cost & Limits

### GitHub Actions Free Tier
- **2,000 minutes/month** for private repos
- **Unlimited** for public repos
- Your workflow uses ~3-5 minutes per run
- Running daily = ~150 minutes/month ✅

### Gemini API Free Tier
- Check current quotas at [Google AI Studio](https://ai.google.dev/)
- Flash models typically have generous free tiers

---

## 🔒 Security Best Practices

- ✅ **Never** commit `.env` file (already in `.gitignore`)
- ✅ Use GitHub Secrets for all credentials
- ✅ Regularly rotate your ManageBac password
- ✅ Monitor workflow runs for suspicious activity
- ✅ Make repository private if it contains school-specific data

---

## 🎯 Next Steps

1. ✅ Test manual workflow trigger
2. ✅ Verify first automated run (tomorrow at 10:00 UTC)
3. ✅ Check ManageBac for submission
4. ✅ Customize schedule if needed
5. ✅ Set up notifications (optional)

---

## 📞 Troubleshooting

If you encounter issues:

1. **Check the workflow logs** - Most errors are clearly logged
2. **Verify secrets** - Wrong credentials are the #1 issue
3. **Test locally first** - Run `python execution/run_if_due.py` on your PC
4. **Review artifacts** - Download and inspect generated files
5. **Update selectors** - ManageBac UI changes may require code updates

---

## 🎉 You're All Set!

Your CAS automation now runs in the cloud 24/7. You can:
- Turn off your PC
- Travel
- Focus on other work

The system will automatically generate and submit reflections every 4 days! 🚀
