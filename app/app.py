import os
import random
import datetime
import re
# import google.generativeai as genai
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Client and Model initialization
client = genai.Client(api_key=os.getenv("API_KEY"))
MODEL_ID = "gemini-2.5-flash"

# for m in client.models.list():
#     print(m.name)

OPERATIONS = {
    "add": (["add", "sum", "+"], lambda x, y: x + y, "sum"),
    "sub": (["subtract", "minus", "-"], lambda x, y: x - y, "difference"),
    "mul": (["multiply", "*", "x"], lambda x, y: x * y, "product"),
    "div": (["divide", "/"], lambda x, y: x / y if y != 0 else "Error: Division by zero", "quotient"),
}

def get_numbers(text, count=2):
    nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
    return nums[:count]

def handle_gemini(prompt):
    try:
        # Updated method call for the new SDK
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {e}"

def process_request(prompt):
    prompt_lower = prompt.lower()

    # Math Check
    for key, (keywords, func, label) in OPERATIONS.items():
        if any(word in prompt_lower for word in keywords):
            nums = get_numbers(prompt_lower)
            if len(nums) >= 2:
                return f"The {label} is: {func(nums[0], nums[1])}"

    # Utility Checks
    if any(w in prompt_lower for w in ["toss", "flip"]):
        result = random.choice(["heads", "tails"])
        return f"The coin landed on: {result.upper()}!"

    if any(w in prompt_lower for w in ["date", "time", "now"]):
        return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Fallback to Gemini
    return handle_gemini(prompt)