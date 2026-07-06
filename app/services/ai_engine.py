"""
==================================================
FinRelief AI
Gemini AI Engine
==================================================
"""

import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def generate_ai_response(prompt: str):
    """
    Generic Gemini AI response generator.
    """

    if model is None:
        return {
            "success": False,
            "message": "Gemini API key not configured."
        }

    try:

        response = model.generate_content(prompt)

        return {
            "success": True,
            "response": response.text
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }