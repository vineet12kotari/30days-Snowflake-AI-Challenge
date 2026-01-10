---

# 📅 Day 2: Running LLMs in Snowflake

Welcome to **Day 2 of #30DaysOfAI** 🤖

Today's goal: Run a **large language model (LLM)** directly within Snowflake using Cortex AI and create a simple chat interface in Streamlit.

---

## 🎯 What We're Building

- Streamlit chat interface
- Snowflake Cortex AI integration
- LLM inference using `AI_COMPLETE` function
- Real-time AI responses in the UI

---

## 📦 Prerequisites

First, install the required libraries:

### For Local Development
Create `requirements.txt`:
```
snowflake-ml-python==1.20.0
snowflake-snowpark-python==1.44.0
```
Then run: `pip install -r requirements.txt`

### For Streamlit Community Cloud
Add the same `requirements.txt` to your GitHub repo

### For Streamlit in Snowflake
Click **Packages** dropdown and add:
- `snowflake-ml-python==1.20.0`
- `snowflake-snowpark-python==1.44.0`

---

## 🧩 The Code

```python
import streamlit as st
from snowflake.snowpark.functions import ai_complete
import json

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Model and prompt
model = "claude-3-5-sonnet"
prompt = st.text_input("Enter your prompt:")

# Run LLM inference
if st.button("Generate Response"):
    df = session.range(1).select(ai_complete(model=model, prompt=prompt).alias("response"))
    
    # Get and display response
    response_raw = df.collect()[0][0]
    response = json.loads(response_raw)
    st.write(response)
```

---

## 🔍 How It Works

1. **Import Libraries** - Streamlit + Snowpark + AI functions
2. **Smart Connection** - Same environment detection as Day 1
3. **Set Model** - Using Claude 3.5 Sonnet from Cortex AI
4. **User Input** - Text box for prompts
5. **AI Processing** - Send prompt to Snowflake Cortex
6. **Parse Response** - Convert JSON response to readable text
7. **Display Result** - Show AI response in the UI

---

## 🤔 Why This Approach?

**`ai_complete()` Function Benefits:**
- Integrates with Snowpark DataFrames
- Perfect for data pipeline workflows
- Runs entirely within Snowflake's secure environment
- No external API calls needed

**The DataFrame Pattern:**
```python
df = session.range(1).select(ai_complete(...))
```
Think of this as creating a single-cell spreadsheet just to run the AI function and capture its output.

---

## 📸 Expected Output

1. Text input box: "Enter your prompt:"
2. Button: "Generate Response"
3. AI response displayed below after clicking

---

## 🧠 Key Learnings

- **Cortex AI Integration** - Running LLMs directly in Snowflake
- **Snowpark Functions** - Using `ai_complete()` for inference
- **JSON Parsing** - Converting AI responses to readable format
- **Secure AI** - No external API keys needed

---

## 🚀 Try These Prompts

- "Explain quantum computing in simple terms"
- "Write a Python function to calculate fibonacci numbers"
- "What are the benefits of using Snowflake for AI?"

---

## 📚 Resources

- [Snowflake Cortex LLM Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [COMPLETE Function Reference](https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex)
- [Available LLM Models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#availability)

---

## 🏷️ Tags
`#30DaysOfAI` `#Streamlit` `#Snowflake` `#CortexAI` `#LLM` `#AI`

---

**Status:** ✅ Day 2 Complete - AI inference running in Snowflake!
