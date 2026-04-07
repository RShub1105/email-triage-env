import os
import json
import requests
from openai import OpenAI

# 1. Setup Environment Variables with Fallbacks
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8b-instruct")
ENV_URL = "http://localhost:7860"

# Initialize Client
# We do this globally, but we'll handle errors during the actual call
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_agent_action(email_text):
    """
    Wraps the LLM call in a try-except block to prevent 
    unhandled exceptions from crashing the script.
    """
    if not email_text:
        return "ignore"

    prompt = f"""
    You are a customer support triage assistant. 
    Classify the following email into exactly one category: "refund", "support", or "ignore".
    
    Email: {email_text}
    
    Respond with ONLY the word of the category.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=30  # Don't hang forever
        )
        content = response.choices[0].message.content
        if content:
            # Clean the output to ensure it's just the word
            prediction = content.strip().lower()
            # Basic validation: ensure it's one of the allowed labels
            if prediction in ["refund", "support", "ignore"]:
                return prediction
        return "ignore" # Default if content is weird
    except Exception as e:
        print(f"[ERROR] LLM Inference failed: {e}")
        return "ignore"  # Critical: Fallback so the script keeps running

def main():
    print("START")

    # Safety check for API Key
    if not API_KEY:
        print("[ERROR] HF_TOKEN is missing! Script will likely fail.")

    tasks = ["easy", "medium", "hard"]
    total_score = 0

    for task in tasks:
        print(f"STEP: Running task = {task}")

        try:
            # 1. Reset Environment
            reset_req = requests.post(f"{ENV_URL}/reset", params={"task": task}, timeout=10)
            reset_req.raise_for_status() # Raise error for 4xx or 5xx
            res = reset_req.json()
            email = res.get("observation", {}).get("email_text", "")

            # 2. Get Prediction (LLM)
            action = get_agent_action(email)
            print(f"STEP: Action predicted = {action}")

            # 3. Submit Step
            requests.post(f"{ENV_URL}/step", json={"action": action}, timeout=10)

            # 4. Get Grade
            grade_req = requests.post(f"{ENV_URL}/grader", json={"action": action}, timeout=10)
            grade_res = grade_req.json()
            score = grade_res.get("score", 0)

            print(f"STEP: Score = {score}")
            total_score += score

        except Exception as e:
            print(f"[ERROR] Error during task '{task}': {e}")
            continue # Move to the next task instead of crashing

    # Final Calculation
    avg_score = total_score / len(tasks)
    print(f"STEP: Final Average Score = {avg_score}")
    print("END")

if __name__ == "__main__":
    main()