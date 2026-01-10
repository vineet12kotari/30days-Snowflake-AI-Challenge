# Day 3 - Write Streams (Snowflake Cortex)
import streamlit as st
import time

st.title(":material/airwave: Write Streams")

# Connect to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(
        st.secrets["connections"]["snowflake"]
    ).create()

# Model selection
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Select a model", llm_models)

prompt = st.text_area("Enter prompt", "What is Python?")

# Streaming option
streaming_method = st.radio(
    "Streaming Method:",
    ["SQL Streaming (Recommended)", "Chunk Simulation"],
)

if st.button("Generate Response"):

    if streaming_method == "SQL Streaming (Recommended)":
        with st.spinner(f"Generating response with `{model}`"):
            query = f"""
            SELECT
                SNOWFLAKE.CORTEX.COMPLETE(
                    '{model}',
                    $$ {prompt} $$
                ) AS RESPONSE
            """

            result = session.sql(query).collect()[0]["RESPONSE"]

            # Simulate token streaming
            output_box = st.empty()
            streamed_text = ""

            for token in result.split():
                streamed_text += token + " "
                output_box.markdown(streamed_text)
                time.sleep(0.03)

    else:
        # Alternative method (manual generator)
        def custom_stream():
            query = f"""
            SELECT
                SNOWFLAKE.CORTEX.COMPLETE(
                    '{model}',
                    $$ {prompt} $$
                ) AS RESPONSE
            """
            result = session.sql(query).collect()[0]["RESPONSE"]
            for word in result.split():
                yield word + " "
                time.sleep(0.03)

        with st.spinner(f"Generating response with `{model}`"):
            st.write_stream(custom_stream)

# Footer
st.divider()
st.caption("Day 3: Write Streams | 30 Days of AI")
