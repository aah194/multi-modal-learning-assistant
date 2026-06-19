from google import genai

def get_answer(
    context,
    question,
    chat_history,
    api_key
):

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are a helpful AI tutor.

Use ONLY the information provided below.

Chat History:
{chat_history}

Context:
{context}

Current Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text