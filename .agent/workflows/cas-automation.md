---
description: Setup and run CAS reflection automation
---

# CAS Reflection Automation Workflow

This workflow automates the creation and submission of CAS reflections to ManageBac using AI.

## Prerequisites

1. **Get Gemini API Key:**
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy it for the next step

2. **Set up environment:**
   ```bash
   cp .env.template .env
   ```
   
3. **Edit `.env` file and add:**
   - Your Gemini API key
   - Your ManageBac school URL (e.g., `https://yourschool.managebac.com`)
   - Your ManageBac username and password

// turbo
4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

// turbo
5. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

## Initial Setup (One-time)

6. **Export your existing CAS reflections:**
   - Manually copy 3-5 of your best past reflections
   - Save them in `.tmp/training_data/reflections.json` in this format:
   ```json
   [
     {
       "title": "Beach Cleanup Activity",
       "type": "Service",
       "date": "2024-10-15",
       "reflection": "Your full reflection text here...",
       "learning_outcomes": ["LO1", "LO5"],
       "approved": true
     }
   ]
   ```

## Running the Workflow

### Option 1: Full Automation (Coming Soon)
Once the scripts are built, you'll run:
```bash
python execution/cas_workflow_orchestrator.py
```

### Option 2: Step-by-Step (Current)

**Step 1: Analyze your activity images**
```bash
python execution/analyze_cas_images.py --images path/to/photo1.jpg path/to/photo2.jpg
```

**Step 2: Generate reflection**
```bash
python execution/generate_reflection.py --activity-data activity_data.json
```

**Step 3: Review and edit**
- Open the generated reflection
- Make any personal adjustments
- Ensure it sounds authentic to you

**Step 4: Submit to ManageBac**
```bash
python execution/submit_to_managebac.py --reflection reflection_draft.json
```

## Development Roadmap

### Phase 1: Core Scripts ✅ (You are here)
- [x] Set up project structure
- [x] Create directive
- [ ] Build `analyze_cas_images.py`
- [ ] Build `generate_reflection.py`
- [ ] Build `submit_to_managebac.py`

### Phase 2: Integration
- [ ] Build orchestrator script
- [ ] Add human review step
- [ ] Test end-to-end workflow

### Phase 3: Enhancement
- [ ] Build simple CLI interface
- [ ] Add batch processing
- [ ] Implement learning outcome suggestions
- [ ] Create submission analytics

## Tips for Best Results

1. **Quality Training Data:** The more of your past reflections you provide, the better the AI matches your style
2. **Always Review:** Never submit without reading and editing
3. **Be Honest:** Only create reflections for real activities you participated in
4. **Iterate:** The system learns from each approved reflection

## Troubleshooting

**Issue: Playwright can't find browser**
```bash
playwright install chromium
```

**Issue: Gemini API errors**
- Check your API key in `.env`
- Verify you have API credits
- Check rate limits

**Issue: ManageBac login fails**
- Verify credentials in `.env`
- Check if 2FA is enabled (requires manual intervention)
- Ensure school URL is correct

## Next Steps

Ask the AI agent to:
1. Build the core execution scripts
2. Test with sample data
3. Refine based on your feedback
