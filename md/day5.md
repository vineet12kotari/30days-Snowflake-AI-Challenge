# 📅 Day 5: LinkedIn Post Generator

Welcome to **Day 5 of #30DaysOfAI** ⚡

Today's goal: Build a **Streamlit web application** that generates professional **LinkedIn posts** using Snowflake's Cortex AI. Users can input a URL, select tone and length, and get AI-generated social media content.

---

## 🎯 What We're Building

- Professional LinkedIn post generator
- URL-based content input
- Customizable tone selection (Professional, Casual, Funny)
- Adjustable word count with slider
- AI-powered content generation via Snowflake Cortex

---

## 🧩 The Complete Code

```python
import streamlit as st
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

# Cached LLM Function
@st.cache_data
def call_cortex_llm(prompt_text):
    """Makes a call to Cortex AI with the given prompt."""
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json

# --- App UI ---
st.title("LinkedIn Post Generator")

# Input widgets
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):
    # Construct the prompt
    prompt = f"""You are an expert social media manager. Generate a LinkedIn post based on the following:

Tone: {tone}
Desired Length: Approximately {word_count} words
Use content from this URL: {content}

Generate only the LinkedIn post text. Use dash for bullet points."""
    
    response = call_cortex_llm(prompt)
    
    st.subheader("Generated Post:")
    st.markdown(response)
```

---

## ⚙️ How It Works: Step-by-Step

### 1. Setup and Snowflake Cortex AI Function

```python
import streamlit as st
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

# Cached LLM Function
@st.cache_data
def call_cortex_llm(prompt_text):
    """Makes a call to Cortex AI with the given prompt."""
    model = "claude-3-5-sonnet"
    df = session.range(1).select(ai_complete(model=model, prompt=prompt_text).alias("response"))
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json
```

- **`import streamlit as st`**: Imports the Streamlit library to create the web application's user interface and logic
- **`from snowflake...ai_complete`**: Imports the `ai_complete` Snowpark function, which is the key to interacting with **Snowflake Cortex AI (LLMs)**
- **`try/except` block**: Automatically detects the environment and connects appropriately (works in SiS, locally, and on Community Cloud)
- **`session`**: The established Snowflake connection, ready to execute operations
- **`@st.cache_data...call_cortex_llm(prompt_text)`**: Defines a function to call the LLM and uses **`@st.cache_data`** to cache its result, preventing re-running the costly AI call every time the app updates, as long as the input (`prompt_text`) remains the same
- **`ai_complete(model=model, prompt=prompt_text)`**: This is the **Snowflake Cortex AI call**, which sends the user's prompt to the specified large language model (e.g., **`claude-3-5-sonnet`**) and returns the generated text

### 2. Building the Streamlit UI and User Input

```python
# --- App UI ---
st.title("LinkedIn Post Generator")

# Input widgets
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):
```

- **`st.title(...)`**: Sets the main title of the web application, making it clear what the app does
- **`st.text_input("Content URL:", ...)`**: Creates a text field where the user can paste the URL of the content they want the LinkedIn post to be about
- **`st.selectbox("Tone:", ...)`**: Provides a dropdown menu for the user to select the desired tone for the generated post
- **`st.slider("Approximate word count:", ...)`**: Offers a slider to let the user easily control the approximate length of the final post
- **`if st.button("Generate Post"):`**: Creates a button; the code block inside the `if` statement will only execute when the user clicks this button

### 3. Prompt Construction and Output Display

```python
# Construct the prompt
prompt = f"""You are an expert social media manager. Generate a LinkedIn post based on the following:

Tone: {tone}
Desired Length: Approximately {word_count} words
Use content from this URL: {content}

Generate only the LinkedIn post text. Use dash for bullet points."""

response = call_cortex_llm(prompt)

st.subheader("Generated Post:")
st.markdown(response)
```

- **`prompt = f"""..."""`**: Constructs the detailed LLM prompt using an **f-string**. This is a critical step, as the prompt includes the **user's inputs** (Tone, Length, URL) and **role-plays** the AI as an "expert social media manager" to guide the output quality
- **`response = call_cortex_llm(prompt)`**: Calls the cached function from Step 1, sending the complete prompt to the Snowflake Cortex AI model and receiving the generated post text
- **`st.subheader("Generated Post:")`**: Adds a smaller heading to clearly delineate the output area for the user
- **`st.markdown(response)`**: Displays the AI-generated post text using Streamlit's `st.markdown`, which allows the response text to be formatted with Markdown syntax (like bold text or bullet points) if the AI includes it

---

## 🎨 User Experience Flow

1. **Enter URL**: User pastes a link to content they want to post about
2. **Select Tone**: Choose from Professional, Casual, or Funny
3. **Set Length**: Use slider to control post length (50-300 words)
4. **Generate**: Click button to create LinkedIn post
5. **Review**: AI-generated post appears with proper formatting

---

## 🧠 Key Features

- **Smart Caching**: Identical inputs return instantly without re-calling AI
- **Flexible Input**: Works with any URL content
- **Tone Control**: Professional for business, Casual for engagement, Funny for viral potential
- **Length Control**: Slider ensures posts fit LinkedIn best practices
- **Expert Prompting**: AI role-plays as social media manager for better output

---

## 📚 Resources

- [Snowflake Cortex LLM Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [st.text_input Documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.text_input)
- [st.selectbox Documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox)
- [st.slider Documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.slider)

---

## 🏷️ Tags

#30DaysOfAI #Streamlit #Snowflake #CortexAI #LinkedIn #SocialMedia #ContentGeneration

**Status**: ✅ Day 5 Complete - Professional LinkedIn post generator with customizable tone and length!
