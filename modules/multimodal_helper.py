from google import genai
from PIL import Image

def multimodal_answer(
    context,
    image_file,
    question,
    api_key
):

    client = genai.Client(
        api_key=api_key
    )

    image = Image.open(
        image_file
    )

    prompt = f"""
You are a helpful AI tutor.

Use the PDF context and image together.

PDF Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text