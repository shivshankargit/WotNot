import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def generate_diwali_greeting(user_name: str, prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = await model.generate_content_async(
            f"Write a warm Diwali greeting for {user_name}. "
            f"Include the message: 'Happy Diwali, I hope you enjoy with your family.' "
            f"Also incorporate this user prompt: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"Error generating greeting: {str(e)}"
