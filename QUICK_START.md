# 🚀 Quick Start Guide - CAS Automation

## ✅ What's Been Created

Your CAS automation system is ready! Here's what you have:

### 📂 Core Scripts
- **`analyze_cas_images.py`** - Analyzes photos using Gemini Vision
- **`generate_reflection.py`** - Generates reflections in your style
- **`submit_to_managebac.py`** - Automates ManageBac submission
- **`cas_workflow_orchestrator.py`** - Main workflow (runs everything)
- **`setup_check.py`** - Validates your setup

### 📚 Training Data
- Located in: `Resala CAS Project trainng/`
- 3 example reflections (your writing style)
- 10 training photos
- Learning outcomes reference

---

## 🔧 Setup Instructions

### Step 1: Install Dependencies

Open PowerShell in this directory and run:

```powershell
pip install -r requirements.txt
```

This installs:
- `google-generativeai` (Gemini API)
- `playwright` (browser automation)
- `python-dotenv` (environment variables)
- `Pillow` (image processing)

### Step 2: Install Playwright Browsers

```powershell
playwright install chromium
```

### Step 3: Configure ManageBac Credentials

1. Copy the contents from `env_config.txt` to a new file called `.env`
2. Edit `.env` and add your ManageBac credentials:

```env
GEMINI_API_KEY=AIzaSyClNIdI1D2jeB7WiI47LWSZ3KbxtlveEXI  # ✅ Already set
MANAGEBAC_URL=https://your-school.managebac.com  # ⚠️ UPDATE THIS
MANAGEBAC_USERNAME=your_username                  # ⚠️ UPDATE THIS
MANAGEBAC_PASSWORD=your_password                  # ⚠️ UPDATE THIS
```

**Important:** Replace:
- `your-school` with your actual school's ManageBac subdomain
- `your_username` with your ManageBac username/email
- `your_password` with your ManageBac password

### Step 4: Verify Setup

Run the setup checker:

```powershell
python execution/setup_check.py
```

This will verify:
- ✅ Python version
- ✅ All dependencies installed
- ✅ .env file configured
- ✅ Training data present
- ✅ Playwright browsers ready

---

## 🎯 Usage

### Option 1: Full Automated Workflow (Recommended)

Run the complete workflow:

```powershell
python execution/cas_workflow_orchestrator.py
```

This will:
1. Ask for activity details
2. Analyze photos (optional)
3. Generate reflection in your style
4. Let you review and edit
5. Submit to ManageBac (with your approval)

### Option 2: Step-by-Step

#### Step 1: Analyze Photos (Optional)

```powershell
python execution/analyze_cas_images.py "path/to/photo1.jpg" "path/to/photo2.jpg"
```

Or use your training photos:

```powershell
python execution/analyze_cas_images.py "Resala CAS Project trainng/Photos training/WhatsApp Image 2025-10-11 at 2.29.26 PM.jpeg"
```

#### Step 2: Generate Reflection

```powershell
python execution/generate_reflection.py
```

This will prompt you for:
- Activity description
- Date
- CAS strand (Creativity/Activity/Service)
- Duration
- Learning outcomes

#### Step 3: Submit to ManageBac

```powershell
python execution/submit_to_managebac.py
```

This will:
- Open a browser window
- Log into ManageBac
- Navigate to CAS section
- Fill in the reflection form
- Pause for your review before submission

---

## 📝 Example Workflow

Here's a complete example:

```powershell
# 1. Run the full workflow
python execution/cas_workflow_orchestrator.py

# When prompted, enter:
# Activity: "Continued organizing donated clothes at Resala Charity"
# Date: "December 1, 2025"
# CAS Strand: "Service"
# Duration: "3"
# Learning Outcomes: "1,4,5"
# Use photos: "y"
# Use training photos: "y"

# 2. Review the generated reflection
# 3. Choose option 1 to submit
# 4. Browser opens - verify and submit
```

---

## 🎨 How It Works

### AI Learning
The system learns from your 3 example reflections:
- **Reflection 1**: Problem identification style
- **Reflection 2**: Challenge and perseverance focus
- **Reflection 3**: Planning and teamwork emphasis

### Writing Style Analysis
Gemini analyzes:
- Your vocabulary and tone
- How you structure reflections
- Your use of specific details
- How you reference learning outcomes
- Mix of English and Arabic terms

### Image Analysis
Gemini Vision examines photos for:
- Activity type and setting
- Number of people involved
- Specific tasks being performed
- Materials and equipment
- Safety concerns or organizational issues
- Teamwork and collaboration

---

## 🔍 What Gets Generated

The AI creates reflections that:
- ✅ Match your personal writing style
- ✅ Include specific details from photos
- ✅ Reference appropriate learning outcomes
- ✅ Maintain authentic voice
- ✅ Follow IB CAS reflection standards

---

## ⚠️ Important Notes

### Always Review
- **Never submit without reading** the generated reflection
- Make edits to ensure authenticity
- Verify learning outcomes are appropriate

### Privacy & Security
- Your `.env` file contains sensitive credentials
- Never share or commit it to version control
- It's already in `.gitignore` for protection

### Academic Integrity
- Only create reflections for **real activities** you participated in
- The AI assists with writing, but experiences must be genuine
- You're responsible for the content submitted

---

## 🐛 Troubleshooting

### "Module not found" error
```powershell
pip install -r requirements.txt
```

### "Playwright browser not found"
```powershell
playwright install chromium
```

### "GEMINI_API_KEY not set"
- Check that `.env` file exists
- Verify the API key is correct
- Make sure there are no extra spaces

### ManageBac login fails
- Verify your credentials in `.env`
- Check if 2FA is enabled (requires manual intervention)
- Ensure school URL is correct

### Reflection doesn't match your style
- Add more example reflections to training data
- Provide more specific activity descriptions
- Edit the generated reflection before submitting

---

## 📊 Files Created During Workflow

After running, you'll find:

```
.tmp/
├── image_analysis.json          # Photo analysis results
├── generated_reflection.json    # Full reflection data
├── generated_reflection.txt     # Text-only version
└── submission_screenshot.png    # Proof of submission
```

---

## 🎓 Next Steps

1. **Run setup check** to verify everything is configured
2. **Test with training data** first to see how it works
3. **Create your first real reflection** for a recent activity
4. **Refine and iterate** based on results

---

## 💡 Tips for Best Results

### For Better Reflections
- Provide detailed activity descriptions
- Use photos that show clear activities
- Be specific about what you did and learned
- Choose appropriate learning outcomes

### For Faster Workflow
- Keep photos organized in folders
- Use consistent naming for activities
- Save common activity descriptions

### For Learning
- Review what the AI generates
- Notice patterns in your writing style
- Improve your own reflection skills

---

## 🆘 Need Help?

If you encounter issues:
1. Run `python execution/setup_check.py` to diagnose
2. Check the error messages carefully
3. Verify your `.env` configuration
4. Make sure training data is in the right location

---

**Ready to start?** Run the setup check first:

```powershell
python execution/setup_check.py
```

Then when everything is green, run your first automation:

```powershell
python execution/cas_workflow_orchestrator.py
```

Good luck with your CAS reflections! 🎉
