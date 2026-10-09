import time
from google.genai import errors
import os
import json
from dotenv import load_dotenv
from google import genai

# 1. The Magic Link: Import your custom function from scraper.py
from scraper import get_chapter_text

# 2. Setup the Environment and API Client
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("System Error: GEMINI_API_KEY is missing! Check your local .env file.")

client = genai.Client()

# 3. Fetch the Raw Data (The Pipeline Starts)
target_url = "https://www.69shuba.com/txt/1364/4697977"
print("\n--- PHASE 1: Fetching Web Novel ---")
novel_text = get_chapter_text(target_url)

# Engineering Check: Did the scraper fail?
if "Error:" in novel_text:
    print("Scraping failed. Exiting program.")
    exit()

# Engineering Trade-off: Truncating the text for the MVP
# Web novel chapters are massive. If we send 5,000 characters to the AI at once, 
# it will take a long time to process and might hit output token limits. 
# For testing, we only send the first 500 characters.
test_snippet = novel_text[:500] 

# 4. Construct the AI Prompt
print("\n--- PHASE 2: Sending to AI for Analysis ---")
prompt = f"""
You are an expert Chinese grammar analyzer. 
Extract all the grammatical structures with HSK level 1 only from the following text:
"{test_snippet}"

Return ONLY a valid JSON array of objects. Do not include any other text or conversational filler.
Each object must have these exact keys:
- "grammar_point": The exact Chinese characters making up the structure.
- "hsk_level": The level string (e.g., "HSK 4").
- "explanation": A 1-sentence explanation of the rule.
"""

# 5. Execute the AI Request with Retry Logic
print("\n--- PHASE 2: Sending to AI for Analysis ---")

max_retries = 3
response = None # Placeholder for our data

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1} to contact AI server...")
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        
        # If the line above succeeds, it skips the 'except' block. 
        # We hit 'break' to immediately exit the loop because we got our data.
        print("Success! Data received.")
        break 
        
    except errors.ServerError as e:
        # This catches the 503 (or 500) server error.
        print(f"Server overloaded. Error: {e}")
        
        if attempt < max_retries - 1:
            print("Waiting 10 seconds before trying again...\n")
            time.sleep(10) # Freezes the script for 10 seconds
        else:
            print("Max retries reached. The server is completely down.")
            exit() # Kills the program so it doesn't crash later

# 6. Parse and Clean the Output
print("\n--- PHASE 3: Parsing Results ---")
try:
    raw_text = response.text.strip().removeprefix('```json').removesuffix('```')
    grammar_points = json.loads(raw_text)
    
    # 7. Display the Final Data
    for item in grammar_points:
        print(f"Grammar: {item['grammar_point']} ({item['hsk_level']})")
        print(f"Rule: {item['explanation']}\n")
        
except json.JSONDecodeError:
    print("Error: The AI did not return perfectly formatted JSON. Here is the raw output:")
    print(response.text)