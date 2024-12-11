import os
import time
import requests

# Set your GitHub credentials and repository details
GITHUB_TOKEN = ""
REPO_OWNER = ""  # GitHub username or org
REPO_NAME = "DeepSpeedExamples"  # Repo name
COMMENT_BODY = "Thank you for submitting this issue! A team member will review it soon."

# API Headers
def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

# Fetch all open issues
def fetch_open_issues():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Post a comment to an issue
def comment_on_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
    payload = {"body": COMMENT_BODY}
    response = requests.post(url, json=payload, headers=get_headers())
    if response.status_code == 201:
        print(f"Commented on issue #{issue_number}.")
    else:
        print(f"Failed to comment on issue #{issue_number}: {response.status_code} - {response.text}")

# Check for new issues and comment
def main():
    commented_issues = set()
    print("GitBot is running locally. Press CTRL+C to stop.")
    while True:
        issues = fetch_open_issues()
        for issue in issues:
            # Skip pull requests, as they also appear in the /issues endpoint
            if "pull_request" in issue:
                continue
            issue_number = issue["number"]
            if issue_number not in commented_issues:
                print(f"Found new issue: #{issue_number}")
                comment_on_issue(issue_number)
                commented_issues.add(issue_number)
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
