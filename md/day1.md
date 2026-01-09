# 📅 Day 1: Connecting Streamlit to Snowflake

Welcome to **Day 1 of #30DaysOfAI** 🚀

Today's goal: Connect a **Streamlit app** to a **Snowflake database** and verify the connection by displaying the Snowflake version.

---

## 🎯 What We're Building

- Streamlit application with Snowflake connection
- Simple validation query to test connectivity
- Success message displaying Snowflake version

---

## 🚀 Getting Started

### 1. Snowflake Setup
Create a **free Snowflake trial account** (120 days of credits):
👉 [Sign up here](https://signup.snowflake.com/?trial=student&cloud=aws&region=us-west-2)

### 2. Connection Setup

#### Option A: Streamlit in Snowflake (Recommended)
- **No setup needed!** 
- Just create a Streamlit app in Snowsight - connection works automatically

#### Option B: Local Development or Streamlit Community Cloud
Create `.streamlit/secrets.toml` in your project folder:

```toml
[connections.snowflake]
account = "xy12345.us-east-1"       # Find in Snowsight → Account → View account details
user = "yourusername"               # Your Snowflake username
password = "yourpassword"           # Your Snowflake password
role = "ACCOUNTADMIN"               # Your role
warehouse = "COMPUTE_WH"            # Your warehouse
database = "SNOWFLAKE_LEARNING_DB"  # Your database
schema = "PUBLIC"                   # Your schema
```

⚠️ **Important:** Add `.streamlit/secrets.toml` to your `.gitignore` file!

---

## 🧩 The Code

```python
import streamlit as st

# Auto-detect environment and connect
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Query and display Snowflake version
version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]
st.success(f"Successfully connected! Snowflake Version: {version}")
```

---

## 🔍 How It Works

1. **Import Streamlit** - Sets up the web app framework
2. **Smart Connection** - Automatically detects if running in Snowflake or locally
3. **Test Query** - Runs `SELECT CURRENT_VERSION()` to verify connection
4. **Success Message** - Displays green confirmation with version number

---

## 📸 Expected Output

✅ Green success message: "Successfully connected! Snowflake Version: [version number]"

---

## 🧠 Key Learnings

- **Environment-aware code** - One codebase works everywhere
- **Snowpark sessions** - Python interface to Snowflake
- **Secure connections** - Using secrets management
- **SQL execution** - Running queries from Python

---

## 📚 Resources

- [Streamlit in Snowflake Docs](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Snowpark Python API](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)

---

## 🏷️ Tags
`#30DaysOfAI` `#Streamlit` `#Snowflake` `#DataConnection` `#AI`

---

**Status:** ✅ Day 1 Complete - Ready for AI development!
