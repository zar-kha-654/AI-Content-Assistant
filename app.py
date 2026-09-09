import os
import streamlit as st
from openai import OpenAI


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)


# --------------------------------------------------
# GROK CLIENT
# --------------------------------------------------

api_key = os.getenv("XAI_API_KEY")

if not api_key:
    st.error("XAI_API_KEY is not configured.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1"
)


# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("✍️ AI Content Assistant")
st.write("Create social media content with Grok AI.")

st.divider()


content_type = st.selectbox(
    "Content Type",
    [
        "Social Media Post",
        "Educational Post",
        "Promotional Post",
        "Announcement",
        "Product Description",
        "Short Article",
        "Thread"
    ]
)


platform = st.selectbox(
    "Platform",
    [
        "LinkedIn",
        "Instagram",
        "Facebook",
        "X (Twitter)",
        "TikTok"
    ]
)


topic = st.text_area(
    "Topic",
    placeholder="Example: Benefits of learning Python"
)


target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: Computer science students"
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Casual",
        "Educational",
        "Inspirational",
        "Persuasive",
        "Funny"
    ]
)


generate = st.button(
    "✨ Generate Content",
    use_container_width=True
)


# --------------------------------------------------
# GENERATE CONTENT
# --------------------------------------------------

if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.warning("Please enter the target audience.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create a complete piece of content using the following requirements:

Content Type: {content_type}
Platform: {platform}
Topic: {topic}
Target Audience: {target_audience}
Tone: {tone}

Your response must contain:

1. A strong title or hook.
2. The complete post/content.
3. A separate caption suitable for the selected platform.
4. 8-12 relevant hashtags.

Make the content engaging, natural, useful, and appropriate for the target audience.

Do not explain your process.
Do not include unnecessary introductions.

Use this exact format:

TITLE:
[title]

POST:
[complete content]

CAPTION:
[caption]

HASHTAGS:
[hashtags]
"""

    with st.spinner("Grok is creating your content..."):

        try:

            response = client.chat.completions.create(
                model="grok-3-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI content assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8
            )

            result = response.choices[0].message.content

            st.divider()
            st.subheader("Generated Content")

            st.markdown(result)

            st.download_button(
                label="⬇️ Download Content",
                data=result,
                file_name="ai_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            st.error(f"Something went wrong: {e}")
