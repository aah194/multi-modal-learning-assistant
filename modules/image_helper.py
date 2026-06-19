from google import genai
from PIL import Image

def analyze_image(
    image_file,
    prompt,
    api_key
):

    client = genai.Client(
        api_key=api_key
    )

    image = Image.open(
        image_file
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text