"""
Smart Catch-up Scheduler.
Checks if a reflection is due (every 4 days) and runs the workflow if needed.
"""

import os
import json
import time
import datetime
import subprocess
from pathlib import Path

# Configuration
INTERVAL_DAYS = 4
LAST_RUN_FILE = Path(".tmp/last_run.json")

def get_last_run() -> float:
    """Get timestamp of last run."""
    if not LAST_RUN_FILE.exists():
        return 0
    try:
        with open(LAST_RUN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('timestamp', 0)
    except:
        return 0

def update_last_run():
    """Update last run timestamp to now."""
    os.makedirs(".tmp", exist_ok=True)
    with open(LAST_RUN_FILE, 'w') as f:
        json.dump({
            'timestamp': time.time(),
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)

def run_workflow():
    """Run the full CAS automation workflow."""
    print("🚀 Starting Autopilot Workflow...")
    
    # 1. Generate Idea
    print("\n[1/3] Generating Idea...")
    result = subprocess.run(["python", "execution/generate_idea.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Idea generation failed: {result.stderr}")
        return False
    print(result.stdout)
    
    # 2. Generate Reflection
    print("\n[2/3] Generating Reflection...")
    result = subprocess.run(["python", "execution/generate_reflection.py", "--auto"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Reflection generation failed: {result.stderr}")
        return False
    print(result.stdout)
    
    # 3. Submit to ManageBac
    print("\n[3/3] Submitting to ManageBac...")
    result = subprocess.run(["python", "execution/submit_to_managebac.py", "--auto"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Submission failed: {result.stderr}")
        return False
    print(result.stdout)
    
    print("\n✅ Workflow Complete!")
    return True

def main():
    print("=" * 60)
    print("CAS AUTOPILOT CHECK")
    print("=" * 60)
    
    last_run = get_last_run()
    now = time.time()
    
    days_since = (now - last_run) / (24 * 3600)
    
    print(f"Last run: {datetime.datetime.fromtimestamp(last_run).strftime('%Y-%m-%d %H:%M:%S') if last_run > 0 else 'Never'}")
    print(f"Time since: {days_since:.2f} days")
    print(f"Interval: {INTERVAL_DAYS} days")
    
    if days_since >= INTERVAL_DAYS:
        print("\n✅ DUE FOR UPDATE! Running workflow...")
        if run_workflow():
            update_last_run()
            print(f"📅 Next run due after: {(datetime.datetime.now() + datetime.timedelta(days=INTERVAL_DAYS)).strftime('%Y-%m-%d')}")
        else:
            print("❌ Workflow failed. Will retry next time.")
    else:
        print("\nzzz Not due yet. Skipping.")

if __name__ == "__main__":
    main()
