# GitHub Actions Setup - Quick Guide

## ✅ Step 1: Code Pushed Successfully!

Your code is now on GitHub: https://github.com/4bdelrahman/Managebac-CAS-automation

---

## 🔑 Step 2: Add GitHub Secrets (5 minutes)

### Open This URL:
👉 **https://github.com/4bdelrahman/Managebac-CAS-automation/settings/secrets/actions**

### Add These 4 Secrets:

Click **"New repository secret"** for each:

| Secret Name | Where to Get Value |
|-------------|-------------------|
| `GEMINI_API_KEY` | From your `.env` file (line with GEMINI_API_KEY) |
| `MANAGEBAC_URL` | From your `.env` file (line with MANAGEBAC_URL) |
| `MANAGEBAC_USERNAME` | From your `.env` file (line with MANAGEBAC_USERNAME) |
| `MANAGEBAC_PASSWORD` | From your `.env` file (line with MANAGEBAC_PASSWORD) |

**Example:**
1. Click "New repository secret"
2. Name: `GEMINI_API_KEY`
3. Value: Copy from your `.env` file (e.g., `AIza...`)
4. Click "Add secret"
5. Repeat for the other 3 secrets

---

## 🚀 Step 3: Test the Workflow

### Option A: Manual Trigger (Recommended First Test)
1. Go to: https://github.com/4bdelrahman/Managebac-CAS-automation/actions
2. Click "CAS Autopilot" (left sidebar)
3. Click "Run workflow" dropdown (right side)
4. Click green "Run workflow" button
5. Refresh after 1 minute to see it running

### Option B: Wait for Automatic Run
- First run: Tomorrow at 10:00 UTC (12:00 PM Egypt time)
- Runs daily, executes workflow every 4 days

---

## 📥 Step 4: Verify Success

After the workflow runs:

1. **Check the logs:**
   - Go to Actions tab
   - Click on the latest workflow run
   - Look for ✅ green checkmarks

2. **Download artifacts:**
   - Scroll to bottom of workflow run page
   - Download "cas-automation-output"
   - Inspect: generated_idea.json, generated_reflection.json, screenshot

3. **Verify on ManageBac:**
   - Log into ManageBac
   - Check your CAS reflections
   - Confirm new entry was added

---

## 🔍 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow fails immediately | Double-check all 4 secrets are added correctly |
| "Login failed" error | Verify MANAGEBAC_USERNAME and MANAGEBAC_PASSWORD |
| "API error" | Check GEMINI_API_KEY is valid and has quota |
| No run yet | Wait until tomorrow 10:00 UTC or trigger manually |

---

## 📊 What Happens Next?

✅ **Automatic Operation:**
- Runs daily at 10:00 UTC
- Checks if 4 days passed since last submission
- If due: generates idea → reflection → submits
- If not: skips until tomorrow
- You can turn off your PC - runs in the cloud!

✅ **Notifications:**
- GitHub emails you if workflow fails
- No email = everything working perfectly!

✅ **Monitoring:**
- Check Actions tab anytime to see history
- Download artifacts to review what was submitted

---

## 🎯 Next Steps

1. [ ] Add the 4 GitHub Secrets (link above)
2. [ ] Manually trigger workflow to test
3. [ ] Verify submission on ManageBac
4. [ ] Relax - automation handles the rest! 🎉

---

Need help? Check [DEPLOYMENT.md](file:///d:/Coding/managebac/DEPLOYMENT.md) for detailed troubleshooting.
