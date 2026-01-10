---

# 📅 Day 3: Streaming LLM Responses

Welcome to **Day 3 of #30DaysOfAI** ⚡

Today's goal: Use the **Snowflake Cortex Python API** to stream LLM responses in real-time, displaying words as they're generated for a better user experience.

---

## 🎯 What We're Building

- Model selection dropdown
- Real-time streaming responses
- Two streaming methods (direct + custom)
- Word-by-word response display

---

## 🧩 The Code

```python
import streamlit as st
from snowflake.cortex import Complete
import time

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Configure UI
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Select a model", llm_models)
example_prompt = "What is Python?"
prompt = st.text_area("Enter prompt", example_prompt)

# Choose streaming method
streaming_method = st.radio("Streaming Method:",
    ["Direct (stream=True)", "Custom Generator"],
    help="Choose how to stream the response")

# Method 1: Direct Streaming
if streaming_method == "Direct (stream=True)":
    if st.button("Generate Response"):
        with st.spinner(f"Generating response with `{model}`"):
            stream_generator = Complete(
                session=session,
                model=model,
                prompt=prompt,
                stream=True  # Built-in streaming
            )
            st.write_stream(stream_generator)

# Method 2: Custom Generator
else:
    def custom_stream_generator():
        """Alternative streaming method for compatibility"""
        output = Complete(
            session=session,
            model=model,
            prompt=prompt  # No stream parameter
        )
        for chunk in output:
            yield chunk
            time.sleep(0.01)  # Small delay for smooth streaming
    
    if st.button("Generate Response"):
        with st.spinner(f"Generating response with `{model}`"):
            st.write_stream(custom_stream_generator)
```

---

## 🔍 How It Works

1. **Import Cortex API** - Direct Python API instead of SQL functions
2. **Model Selection** - Dropdown with multiple LLM options
3. **Streaming Methods** - Two approaches for real-time responses
4. **Real-time Display** - Words appear as they're generated

---

## ⚡ Streaming Methods Explained

### Method 1: Direct Streaming (`stream=True`)
- **Simplest approach** - Built-in streaming support
- **When to use** - When API streaming works directly with Streamlit
- **Benefits** - Clean, minimal code

### Method 2: Custom Generator
- **Compatibility mode** - Manual chunk yielding with delays
- **When to use** - When direct streaming has compatibility issues
- **Benefits** - More reliable for complex scenarios

---

## 🚀 Why Streaming Matters

**Without Streaming:**
- Users see blank screen for seconds
- Feels slow and unresponsive
- Poor user experience

**With Streaming:**
- Words appear immediately
- Feels fast and interactive
- Same total time, better perception

---

## 📸 Expected Output

1. Model dropdown: Claude, Mistral, Llama options
2. Text area with example prompt
3. Radio buttons for streaming method
4. Real-time word-by-word response display

---

## 🧠 Key Learnings

- **Cortex Python API** - Direct programmatic access vs SQL functions
- **Streaming UX** - Real-time responses improve perceived performance
- **Generator Functions** - Custom streaming for compatibility
- **Multiple Models** - Easy model switching in one app

---

## 🆚 Day 2 vs Day 3

| Feature | Day 2 (`ai_complete`) | Day 3 (`Complete`) |
|---------|----------------------|-------------------|
| **API Style** | SQL function | Python class |
| **Streaming** | No | Yes |
| **Response** | JSON parsing needed | Direct text |
| **Use Case** | Data pipelines | Interactive apps |

---

## 📚 Resources

- [Cortex Complete Python API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#complete)
- [st.write_stream Documentation](https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream)

---

## 🏷️ Tags
`#30DaysOfAI` `#Streamlit` `#Snowflake` `#CortexAI` `#Streaming` `#UX`

---

**Status:** ✅ Day 3 Complete - Real-time AI streaming implemented!
