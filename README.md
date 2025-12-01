# ManageBac Project

This project follows a 3-layer architecture for AI-assisted automation:

## Directory Structure

```
managebac/
├── .tmp/              # Temporary/intermediate files (not committed)
├── execution/         # Python scripts (deterministic execution layer)
├── directives/        # SOPs in Markdown (instruction layer)
├── .env              # Environment variables (not committed)
├── .gitignore        # Git ignore rules
└── GEMINI.md         # Agent operating instructions
```

## Setup

1. **Copy environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Add your API keys to `.env`:**
   - Hunter.io API key
   - Google OAuth credentials (if needed)
   - Other service credentials

3. **Install Python dependencies** (as needed):
   ```bash
   pip install -r requirements.txt
   ```

## Architecture Layers

**Layer 1: Directives** (`directives/`)
- Natural language SOPs defining what to do
- Goals, inputs, tools, outputs, edge cases

**Layer 2: Orchestration** (AI Agent)
- Intelligent routing and decision making
- Reads directives, calls execution scripts
- Handles errors and updates directives

**Layer 3: Execution** (`execution/`)
- Deterministic Python scripts
- API calls, data processing, file operations
- Reliable, testable, fast

## Workflow

1. Check for existing tools in `execution/`
2. Read relevant directive from `directives/`
3. Execute scripts with proper inputs
4. Handle errors and self-anneal
5. Update directives with learnings

## File Organization

- **Deliverables**: Google Sheets, Slides, or other cloud outputs
- **Intermediates**: `.tmp/` directory (regenerated as needed)

Everything in `.tmp/` can be deleted and regenerated.
