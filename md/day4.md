# 📅 Day 4: Snowflake Cortex LLM Web App

Welcome to **Day 4 of #30DaysOfAI** ⚡

Today's goal: Build a **Streamlit web application** that calls a Snowflake Cortex Large Language Model, measures response times, and uses smart caching for better performance.

---

## 🎯 What We're Building

- Clean web interface with text input
- AI-powered responses from Claude 3.5 Sonnet
- Response time measurement
- Smart caching for identical prompts
- Error handling and user feedback

---

## 🧩 The Code

```python
import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Define the Cortex LLM call
@st.cache_data
def call_cortex_llm(prompt_text):
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json

# Build the web app interface
st.title("❄️ Snowflake Cortex LLM Chat")

prompt = st.text_input("Enter your prompt", "Why is the sky blue?")

if st.button("Submit"):
    start_time = time.time()
    response = call_cortex_llm(prompt)
    end_time = time.time()
    
    st.success(f"*Call took {end_time - start_time:.2f} seconds*")
    st.write(response)
```

---

## 🔍 How It Works: Step-by-Step

### 1. Setup: Imports and Session

```python
import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
```

- **Import libraries**: streamlit for web UI, time for measuring speed, json to parse responses, snowpark for Snowflake connection
- **Auto-connection**: Detects environment and connects appropriately - works everywhere

### 2. Defining the Cortex LLM Call

```python
@st.cache_data
def call_cortex_llm(prompt_text):
    model = "claude-3-5-sonnet"
    df = session.range(1).select(ai_complete(model=model, prompt=prompt_text).alias("response"))
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json
```

- **@st.cache_data**: Smart caching - identical prompts return instantly (0.1s vs 3-5s)
- **ai_complete(...)**: Core Snowpark function calling Claude 3.5 Sonnet in Snowflake Cortex
- **df.collect()[0][0]**: Executes query and extracts the response text
- **json.loads(...)**: Parses JSON response into Python dictionary

### 3. Building the Web App Interface

```python
prompt = st.text_input("Enter your prompt", "Why is the sky blue?")

if st.button("Submit"):
    start_time = time.time()
    response = call_cortex_llm(prompt)
    end_time = time.time()
    
    st.success(f"*Call took {end_time - start_time:.2f} seconds*")
    st.write(response)
```

- **st.text_input(...)**: Creates input box with default text
- **if st.button("Submit")**: Code runs only when button is clicked
- **Time measurement**: Captures before/after timestamps for performance tracking
- **st.success(...)**: Shows green timing message
- **st.write(response)**: Displays the AI response

---

## ⚡ Smart Caching Explained

**First time** submitting "Why is the sky blue?":
- Calls Snowflake Cortex → 3.2 seconds
- Response cached automatically

**Second time** submitting same prompt:
- Returns cached result → 0.08 seconds
- **40x faster!**

**Different prompt** "What is Python?":
- New prompt = cache miss → 2.9 seconds
- This response now cached too

---

## 🚀 Performance Benefits

### Without Caching:
- Every identical question takes 3-5 seconds
- Wastes compute resources
- Poor user experience

### With Caching:
- Identical questions return instantly
- Saves Snowflake credits
- Feels responsive and fast

---

## 📸 Expected Output

- Clean web interface with title and input box
- Submit button that triggers AI call
- Timing display showing response speed
- AI response formatted and displayed below
- Instant responses for repeated prompts

---

## 🧠 Key Learnings

- **ai_complete Function** - SQL-based LLM calls in Snowpark
- **Smart Caching** - @st.cache_data dramatically improves performance
- **JSON Parsing** - LLM responses need parsing for clean display
- **Environment Detection** - Code works locally and in Snowflake
- **Performance Measurement** - Users love seeing response times

---

## 🆚 Day 3 vs Day 4

| Feature | Day 3 (Streaming) | Day 4 (Web App) |
|---------|------------------|-----------------|
| Focus | Real-time streaming | Complete web interface |
| API | Complete class | ai_complete function |
| Caching | No | Yes (@st.cache_data) |
| Timing | No | Yes (performance tracking) |
| UI | Basic | Polished web app |

---

## 📚 Resources

- [st.cache_data Documentation](https://docs.streamlit.io/library/api-reference/performance/st.cache_data)
- [Caching in Streamlit](https://docs.streamlit.io/library/advanced-features/caching)
- [SiS Caching Limitations](https://docs.streamlit.io/knowledge-base/using-streamlit/caching-issues)

---

## 🏷️ Tags

#30DaysOfAI #Streamlit #Snowflake #CortexAI #WebApp #Caching

**Status**: ✅ Day 4 Complete - Full-featured LLM web app with smart caching!
