import subprocess
from datetime import datetime, timezone
import random

#repo url on github
Repo="https://github.com/karankoder/FideX"

#timestamp to start the first commit
timestamp=1742835646

# No of commits not to change from start
no_of_commits_not_to_change=0

#path to the repo
path="/Users/jineshjain/Desktop/FideX"
def format_time(unix_timestamp):
    dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    return dt.isoformat()

def run_command(cmd):
    """Helper function to run shell commands."""
    result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True,cwd=f'{path}')
    return result.stdout.strip()

# Step 1: Get all commit hashes (oldest first)
run_command("pwd")
commit_hashes = run_command("git rev-list --reverse HEAD").split("\n")

# Step 2: Iterate through commits and change timestamps
commit_count=len(commit_hashes)

for i in range(commit_count):
    if(i<no_of_commits_not_to_change):
        continue
    commit_hash = commit_hashes[i]
    print(f"Rewriting commit: {commit_hash}")
    tz_offset = "+0530"  # IST timezone (adjust as needed)
    date_str = f'b"{timestamp} {tz_offset}"'

    # Randomly adjust the timestamp for demonstration
    
    # Checkout the commit in interactive rebase mode
    # Modify commit date and re-commit
    command = f"""git filter-repo --commit-callback '
    if commit.original_id == b"{commit_hash}":  # Use dynamic commit hash
        commit.author_date = {date_str}
        commit.committer_date = {date_str}
    '"""
    run_command(command)
    commit_hashes = run_command("git rev-list --reverse HEAD").split("\n")

    #randomly add time from 30 minutes to 2 hours
    random_number = random.randint(30*60, 120*60)
    timestamp+=random_number
    # break

# Step 3: Checkout back to the main branch
run_command("git checkout main")  # Change 'main' to your branch name

# Step 4: Force push (Be careful, this rewrites history)
print("Force pushing changes (Warning: This rewrites history!)")

run_command(f"git remote add origin {Repo}")
run_command("git push origin main --force")

print("All commits have been updated successfully!")
