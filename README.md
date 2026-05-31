# 🏴‍☠️ DevPulse — AI-Powered Daily Standup Agent

> Built for the **Pirates of the Coral-bean Hackathon** by WeMakeDevs  
> Powered by **Coral** + **Groq AI (LLaMA 3)**

---

## 👋 Hey, We're Glad You're Here

We're Pravallika and Pramodh varma — two students who decided to join this hackathon with zero prior experience building AI agents. Honestly? We had no idea what we were getting into. But we figured it out, one error message at a time.

This is DevPulse. We're really proud of it.

---

## 😤 The Problem We Noticed

Every single day, software teams sit through a standup meeting that goes something like this:

> *"Yesterday I worked on PR #45... there's a Sentry error blocking it... and someone mentioned it in Slack but I can't find the message..."*

Meanwhile, all that information **already exists** — on GitHub, on Sentry, on Slack. Nobody is missing it. It's just scattered across three different platforms that don't talk to each other.

So engineers waste **20–30 minutes every morning** manually collecting information that a computer could fetch in 10 seconds.

That felt wrong to us. So we fixed it.

---

## 💡 What DevPulse Does

DevPulse is an AI agent that:

1. **Connects to GitHub** → fetches your open issues and pull requests
2. **Connects to Sentry** → checks for active production errors
3. **Connects to Slack** → reads recent team discussions
4. **Joins all this data** using Coral's SQL engine
5. **Sends everything to Groq AI** → which writes a clean, structured standup report
6. **Delivers it in seconds** → through a simple web interface anyone can use

No more switching between tabs. No more "I forgot to check Sentry." No more 30-minute standups for information that already existed.

---

## 🪸 Why Coral is the Heart of This Project

Before Coral, doing what DevPulse does would require:
- Writing a GitHub API integration
- Writing a Sentry API integration  
- Writing a Slack API integration
- Handling authentication for all three
- Dealing with pagination, rate limits, data formatting

That's weeks of work.

With Coral, we write **one SQL query** that spans all three platforms simultaneously:

```sql
SELECT issues.title, errors.message, channels.name
FROM github.issues
JOIN sentry.issues ON ...
JOIN slack.channels ON ...
WHERE issues.state = 'open'
```

Coral handles everything behind the scenes — authentication, API calls, data joining, pagination. We just get clean data back and hand it to the AI.

That's the magic. That's why we chose Coral.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| 🪸 Coral | Multi-source SQL data layer — the core of everything |
| 🐍 Python 3.10 | Main programming language |
| 🤖 Groq AI (LLaMA 3) | Free LLM that generates the standup report |
| 🌐 Streamlit | Simple web interface |
| 🐙 GitHub | Source control + one of our data sources |
| 🚨 Sentry | Production error monitoring data source |
| 💬 Slack | Team communication data source |

---

## 🚀 How to Run It Yourself

### 1. Install Coral
```bash
# Windows
winget install withcoral.coral

# Mac/Linux
curl -fsSL https://withcoral.com/install.sh | sh
```

### 2. Clone This Repo
```bash
git clone https://github.com/pravalli1309/devpulse-agent.git
cd devpulse-agent
```

### 3. Set Up Python Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 4. Connect Your Data Sources
```bash
coral source add github --token YOUR_GITHUB_TOKEN
coral source add sentry --token YOUR_SENTRY_TOKEN --org YOUR_ORG
coral source add slack --token YOUR_SLACK_TOKEN
```

### 5. Add Your API Key
Create a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
```

### 6. Run the App
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Enter your repo details. Click Generate. Watch the magic. 🎉

---

## 📺 Demo Video

[▶️ Watch DevPulse in Action -> https://www.loom.com/share/9acc91a269b64eeb97678ce487065dba](#)

---

## 🗂️ Project Structure

```
devpulse-agent/
│
├── agent.py          # Core AI agent — queries Coral, calls Groq AI
├── app.py            # Streamlit web interface
├── requirements.txt  # Python dependencies
├── .env              # Your API keys (never committed to GitHub)
├── .gitignore        # Keeps secrets safe
└── README.md         # You are here!
```

---

## 🧠 How It Actually Works (For the Curious)

```
User clicks "Generate Report"
        ↓
app.py calls run_agent()
        ↓
agent.py sends SQL queries to Coral
        ↓
Coral calls GitHub API + Sentry API + Slack API simultaneously
        ↓
Clean data comes back to agent.py
        ↓
All data is sent to Groq AI (LLaMA 3) with a prompt
        ↓
Groq AI writes a structured standup report
        ↓
Report appears on screen in seconds ✨
```

---

## 😅 Honest Challenges We Faced

We won't pretend this was smooth. Here's what actually happened:

- **Windows encoding errors** — Coral was returning data with special characters that Python couldn't read. Fixed by adding `encoding="utf-8"` to subprocess calls.
- **Wrong table names** — Coral uses `github.pulls` not `github.pull_requests`. Took us a while to figure that out.
- **Gemini API not working in India** — Google AI Studio gave us an OAuth token instead of an API key. Switched to Groq, which worked perfectly and is completely free.
- **Git not installed** — Had to install it mid-hackathon. Every step was a new learning.

We're first year students. This was our first AI agent. We learned more in these 2 days than in months of classes.

---

## 🔮 What's Next for DevPulse

If we keep building this:

- 📧 **Auto-email reports** every morning before standup
- 📅 **Jira integration** for project management data
- 📊 **Weekly trend reports** — are errors increasing? PRs getting slower?
- 🔔 **Slack bot** that posts the report directly into your channel
- 🌍 **Multi-team support** for larger organizations

---

## 👥 Team

| Name | Role | GitHub |
|---|---|---|
| Jyothi Pravallika | Lead Developer & Agent Architecture | [@pravalli1309](https://github.com/pravalli1309) |
| Pramodh Varma | Co Developer  | [@Pramodhvarma2007](https://github.com/Pramodhvarma2007) |

---

## Thank You

To **WeMakeDevs** for organizing this hackathon.  
To **Coral** for making multi-source data feel like magic.  
To **Groq** for giving students free access to powerful AI.  
And to everyone who told us "just try it" — you were right.

---

*Built with a lot of ☕, many error messages, and zero sleep during the Pirates of the Coral-bean Hackathon 2026 🏴‍☠️*
