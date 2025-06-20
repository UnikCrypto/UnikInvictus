import os
import openai
from dotenv import load_dotenv


# Resolve paths relative to this file so the script works from any
# working directory and from different repository layouts (either placed
# in the repo root or in a ``scripts`` subfolder).
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))

# Try loading ``config/.env`` from the current directory first and then
# from the parent directory. This ensures the API key is picked up
# regardless of where the script resides.
for directory in (THIS_DIR, PARENT_DIR):
    env_path = os.path.join(directory, "config", ".env")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        break

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.strip() == "":
    raise ValueError("OpenAI API key is missing. Please check your .env file.")

# Configure the OpenAI package globally for convenience
openai.api_key = api_key

SYSTEM_MESSAGE = "You are a helpful assistant that writes marketing video scripts."

def generate_script(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate a short marketing video script using OpenAI models.

    The function first tries a chat-based completion using ``model``. If the
    project does not have access to that model (for example a 403 or model not
    found error), it falls back to ``text-davinci-003``.
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except (openai.PermissionDeniedError, openai.NotFoundError):
        # Fallback for API keys that cannot access chat models
        completion = openai.completions.create(
            model="text-davinci-003",
            prompt=f"{SYSTEM_MESSAGE}\n{prompt}",
            max_tokens=500,
        )
        return completion.choices[0].text.strip()

if __name__ == "__main__":
    input_prompt_path = os.path.join(THIS_DIR, "input", "prompt.txt")
    output_script_path = os.path.join(THIS_DIR, "output", "generated_script.txt")

    if not os.path.exists(input_prompt_path):
        raise FileNotFoundError(f"Prompt file not found at {input_prompt_path}")

    with open(input_prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    script = generate_script(prompt)

    os.makedirs(os.path.dirname(output_script_path), exist_ok=True)
    with open(output_script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print("✅ Script generat cu succes:", output_script_path)
