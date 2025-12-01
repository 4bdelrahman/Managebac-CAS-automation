# Automate ManageBac CAS Reflections

## Goal
Automate the creation and submission of CAS (Creativity, Activity, Service) reflections on ManageBac for IB students, using AI to generate personalized reflections based on provided evidence (photos, text, previous reflections).

## Background Context
ManageBac is the IB school management platform where students must submit CAS reflections. The platform:
- Does NOT have a student-accessible API (admin-only)
- Requires manual web form submission
- Accepts evidence: photos, videos, files, website links
- Requires reflections to be linked to learning outcomes
- Needs CAS advisor approval

**Important Legal/Ethical Note:** This automation is for **personal use only** to help manage your own CAS submissions. It does not violate terms of service when used responsibly for your own account.

## Inputs
1. **CAS Experience Data:**
   - Photos/videos from the activity
   - Text description of what you did
   - Date and duration
   - Activity type (Creativity/Activity/Service)
   - Learning outcomes to link

2. **Training Data:**
   - Your previous approved CAS reflections (to learn your writing style)
   - Your personal reflection preferences
   - Tone and depth preferences

3. **ManageBac Credentials:**
   - School ManageBac URL
   - Username/password (stored securely in `.env`)

## Tools & Technologies

### Layer 1: AI Reflection Generation
**Tool:** Google Gemini API (or OpenAI GPT-4)
- **Why:** You're already using Gemini, and it excels at:
  - Analyzing images to understand activities
  - Learning from your previous writing style
  - Generating authentic, personalized reflections
  - Adapting tone based on your preferences

**Alternative:** OpenAI GPT-4 Vision (if you prefer)

### Layer 2: Browser Automation
**Tool:** Playwright (Python) or Puppeteer (Node.js)
- **Why Playwright over Selenium:**
  - More modern and reliable
  - Better handling of dynamic content
  - Built-in screenshot/video recording
  - Easier to debug
  - Supports multiple browsers
  - Better documentation

**Recommendation:** Use **Playwright with Python** since it integrates well with the Gemini API

### Layer 3: Data Storage & Training
**Tool:** Local JSON files + Vector embeddings
- Store your previous reflections in `.tmp/training_data/`
- Use embeddings to find similar past reflections
- Learn your writing patterns over time

### Layer 4: Image Analysis
**Tool:** Gemini Vision API
- Analyze photos to extract activity details
- Identify people, locations, activities
- Generate context for reflections

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INPUT PHASE                                              │
│ - Upload photos/videos                                      │
│ - Provide basic info (date, type, duration)                 │
│ - Select learning outcomes                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. AI ANALYSIS PHASE                                        │
│ - Gemini Vision analyzes images                             │
│ - Extracts activity context                                 │
│ - Retrieves similar past reflections (RAG)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. REFLECTION GENERATION                                    │
│ - Gemini generates reflection in your style                 │
│ - Links to learning outcomes                                │
│ - Maintains authenticity and personal voice                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. REVIEW & EDIT (HUMAN IN THE LOOP)                        │
│ - You review the generated reflection                       │
│ - Make any edits/adjustments                                │
│ - Approve for submission                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. AUTOMATED SUBMISSION (Playwright)                        │
│ - Login to ManageBac                                        │
│ - Navigate to CAS section                                   │
│ - Fill in form fields                                       │
│ - Upload evidence files                                     │
│ - Submit reflection                                         │
└─────────────────────────────────────────────────────────────┘
```

## Outputs
1. **Generated Reflection:** Personalized text ready for submission
2. **Submission Confirmation:** Screenshot/proof of successful submission
3. **Training Data Update:** Approved reflection added to your style database
4. **Logs:** Record of all submissions in `.tmp/submission_logs/`

## Implementation Steps

### Phase 1: Setup (Week 1)
1. Install dependencies:
   - `playwright` (browser automation)
   - `google-generativeai` (Gemini API)
   - `python-dotenv` (environment variables)
   - `pillow` (image processing)

2. Set up API keys in `.env`:
   - `GEMINI_API_KEY`
   - `MANAGEBAC_URL`
   - `MANAGEBAC_USERNAME`
   - `MANAGEBAC_PASSWORD`

3. Create training data structure:
   - Export your existing CAS reflections from ManageBac
   - Store in `.tmp/training_data/reflections.json`

### Phase 2: Build Core Scripts (Week 2)
1. **`execution/analyze_cas_images.py`**
   - Takes image inputs
   - Uses Gemini Vision to extract context
   - Returns structured activity data

2. **`execution/generate_reflection.py`**
   - Loads training data (your past reflections)
   - Uses RAG to find similar experiences
   - Generates reflection in your style
   - Returns draft reflection

3. **`execution/submit_to_managebac.py`**
   - Uses Playwright to automate browser
   - Logs into ManageBac
   - Fills CAS reflection form
   - Uploads evidence
   - Submits and captures confirmation

### Phase 3: Integration & Testing (Week 3)
1. **`execution/cas_workflow_orchestrator.py`**
   - Main script that ties everything together
   - Handles the full workflow
   - Includes human review step

2. Test with a few sample CAS experiences
3. Refine prompts based on output quality

### Phase 4: Enhancement (Ongoing)
1. Build a simple CLI or web interface
2. Add batch processing for multiple experiences
3. Implement learning outcome suggestion
4. Create analytics dashboard for CAS hours

## Edge Cases & Considerations

### Technical Challenges
1. **ManageBac UI Changes:** 
   - Playwright selectors may break if ManageBac updates
   - Solution: Use robust selectors (data-testid, ARIA labels)
   - Keep screenshots of the UI for reference

2. **Two-Factor Authentication:**
   - If your school uses 2FA, you'll need manual intervention
   - Solution: Use Playwright in headed mode, pause for 2FA

3. **Rate Limiting:**
   - Don't spam submissions
   - Solution: Add delays, respect the platform

### Quality Control
1. **Authenticity:** Always review AI-generated reflections
2. **Learning Outcomes:** Ensure they genuinely match your activity
3. **Evidence:** Upload real photos/videos from your experiences

### Ethical Guidelines
1. **Personal Use Only:** This is for YOUR reflections, not others
2. **Honest Reflections:** AI should enhance, not fabricate
3. **Review Everything:** Never submit without reading
4. **Academic Integrity:** The reflections should represent real experiences

## Success Metrics
- Time saved: Target 70% reduction in reflection writing time
- Quality: Reflections should match or exceed your manual quality
- Approval rate: Maintain high CAS advisor approval rate
- Learning: System improves with each reflection

## Maintenance
- Update training data after each approved reflection
- Monitor ManageBac for UI changes
- Refine prompts based on feedback
- Keep dependencies updated

## Next Steps
1. Review this directive with the AI agent
2. Decide on specific implementation details
3. Set up development environment
4. Start with Phase 1 (Setup)
5. Build incrementally, test thoroughly
