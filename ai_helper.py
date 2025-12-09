# ai_helper.py
import os

try:
    from openai import OpenAI
except:
    OpenAI = None

def get_it_insight_from_ai(summary_text: str) -> str:
    """
    Sends ticket summary text to OpenAI and returns an insight.
    Requires OPENAI_API_KEY environment variable.
    """

    if OpenAI is None:
        return "OpenAI library not installed. Install 'openai' package."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY not set. AI feature disabled."

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an IT operations assistant. Based on this summary of ticket data:

{summary_text}

Explain in simple terms:
1) Where the biggest delays are (by staff or status)
2) One or two actions the IT manager should take.
Keep it short and practical.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"
