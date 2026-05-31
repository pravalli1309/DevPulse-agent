import streamlit as st
from agent import run_agent

# ── Page Setup ──────────────────────────────
st.set_page_config(
    page_title="DevPulse",
    page_icon="🏴‍☠️",
    layout="centered"
)

# ── Header ───────────────────────────────────
st.title("🏴‍☠️ DevPulse")
st.markdown("### AI-Powered Daily Standup Generator")
st.markdown("*Powered by **Coral** + **Groq AI** — Built for Pirates of the Coral-bean Hackathon*")
st.divider()

# ── Sidebar ──────────────────────────────────
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("Fill in your project details below:")

repo_owner = st.sidebar.text_input(
    "GitHub Username",
    value="pravalli1309"
)

repo_name = st.sidebar.text_input(
    "Repository Name",
    value="devpulse-agent"
)

slack_channel = st.sidebar.text_input(
    "Slack Channel",
    value="all-devpulse"
)

st.sidebar.divider()
st.sidebar.markdown("### 🔌 Connected Sources")
st.sidebar.success("✅ GitHub")
st.sidebar.success("✅ Sentry")
st.sidebar.success("✅ Slack")
st.sidebar.divider()
st.sidebar.markdown("### ⚡ Powered By")
st.sidebar.markdown("🪸 **Coral** — Multi-source SQL")
st.sidebar.markdown("🤖 **Groq AI** — LLaMA 3 Model")

# ── Main Section ─────────────────────────────
st.markdown("### How it works:")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Step 1** 🪸\nCoral queries GitHub, Sentry & Slack using SQL")
with col2:
    st.info("**Step 2** 🤖\nGroq AI reads all the data and understands it")
with col3:
    st.info("**Step 3** 📋\nA clean standup report is generated instantly")

st.divider()

# ── Generate Button ───────────────────────────
if st.button("🚀 Generate Standup Report", type="primary", use_container_width=True):
    if not repo_owner or not repo_name:
        st.error("⚠️ Please fill in GitHub Username and Repository Name in the sidebar!")
    else:
        with st.spinner("🔍 Querying GitHub, Sentry & Slack via Coral..."):
            try:
                report = run_agent(repo_owner, repo_name, slack_channel)

                st.success("✅ Report Generated Successfully!")
                st.divider()

                st.markdown("## 📋 Your Standup Report")
                st.markdown(report)
                st.divider()

                # Download button
                st.download_button(
                    label="📥 Download Report as .txt",
                    data=report,
                    file_name="standup_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {str(e)}")
                st.markdown("Check your terminal for more details.")

# ── Footer ────────────────────────────────────
st.divider()
st.markdown(
    "<center>Built with ❤️ for Pirates of the Coral-bean Hackathon 🏴‍☠️ | WeMakeDevs</center>",
    unsafe_allow_html=True
)