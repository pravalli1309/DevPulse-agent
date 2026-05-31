import subprocess
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Connect to Groq (free!)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─────────────────────────────────────────
# CORAL QUERY FUNCTION
# ─────────────────────────────────────────
def query_coral(sql: str) -> list:
    result = subprocess.run(
        ["coral", "sql", "--format", "json", sql],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if result.returncode != 0:
        print(f"⚠️ Coral error: {result.stderr}")
        return []
    if not result.stdout or result.stdout.strip() == "":
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

# ─────────────────────────────────────────
# GITHUB DATA
# ─────────────────────────────────────────
def get_open_prs(repo_owner: str, repo_name: str) -> list:
    sql = f"""
        SELECT number, title, state, created_at, user__login
        FROM github.pulls
        WHERE owner = '{repo_owner}'
        AND repo = '{repo_name}'
        AND state = 'open'
        ORDER BY created_at DESC
        LIMIT 10
    """
    return query_coral(sql)

def get_open_issues(repo_owner: str, repo_name: str) -> list:
    sql = f"""
        SELECT number, title, state, created_at, user__login
        FROM github.issues
        WHERE owner = '{repo_owner}'
        AND repo = '{repo_name}'
        AND state = 'open'
        ORDER BY created_at DESC
        LIMIT 10
    """
    return query_coral(sql)

# ─────────────────────────────────────────
# SENTRY DATA
# ─────────────────────────────────────────
def get_sentry_errors() -> list:
    sql = """
        SELECT title, count, last_seen, level, status
        FROM sentry.issues
        WHERE status = 'unresolved'
        ORDER BY last_seen DESC
        LIMIT 10
    """
    return query_coral(sql)

# ─────────────────────────────────────────
# SLACK DATA
# ─────────────────────────────────────────
def get_slack_messages(channel: str) -> list:
    sql = f"""
        SELECT id, name, topic, purpose, num_members
        FROM slack.channels
        WHERE name = '{channel}'
        LIMIT 10
    """
    return query_coral(sql)

# ─────────────────────────────────────────
# GROQ AI — Generate the Report
# ─────────────────────────────────────────
def generate_report(prs, issues, errors, messages) -> str:
    prompt = f"""
You are DevPulse, an AI assistant for software engineering teams.
Generate a clear, friendly daily standup report based on this data.
Use emojis and clear sections. Highlight anything urgent.

OPEN PULL REQUESTS (GitHub):
{json.dumps(prs, indent=2) if prs else "No open PRs found."}

OPEN ISSUES (GitHub):
{json.dumps(issues, indent=2) if issues else "No open issues found."}

PRODUCTION ERRORS (Sentry):
{json.dumps(errors, indent=2) if errors else "No active errors found."}

RECENT SLACK MESSAGES:
{json.dumps(messages, indent=2) if messages else "No recent messages found."}

Write a standup report with these sections:
1. 🔀 Pull Requests Status
2. 🐛 Open Issues
3. 🔥 Production Errors
4. 💬 Team Discussion Highlights
5. ⚠️ Blockers & Urgent Items

End with one short motivational line for the team.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free model on Groq
        messages=[
            {
                "role": "system",
                "content": "You are DevPulse, an AI standup report generator for software teams."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1500
    )

    return response.choices[0].message.content

# ─────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────
def run_agent(repo_owner: str, repo_name: str, slack_channel: str) -> str:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🏴‍☠️  DevPulse Agent Starting...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🔍 Fetching open PRs from GitHub...")
    prs = get_open_prs(repo_owner, repo_name)
    print(f"   ✅ Found {len(prs)} open PRs")

    print("🐛 Fetching open issues from GitHub...")
    issues = get_open_issues(repo_owner, repo_name)
    print(f"   ✅ Found {len(issues)} open issues")

    print("🚨 Fetching errors from Sentry...")
    errors = get_sentry_errors()
    print(f"   ✅ Found {len(errors)} active errors")

    print("💬 Fetching Slack messages...")
    messages = get_slack_messages(slack_channel)
    print(f"   ✅ Found {len(messages)} messages")

    print("🤖 Generating report with Groq AI...")
    report = generate_report(prs, issues, errors, messages)

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 DAILY STANDUP REPORT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(report)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return report


if __name__ == "__main__":
    run_agent(
        repo_owner="pravalli1309",
        repo_name="DevPulse-agent",
        slack_channel="all-devpulse"
    )