import os
import openai
from dotenv import load_dotenv

# Always resolve paths relative to this file so the script works from any
# working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, "config/.env"))
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.strip() == "":
    raise ValueError("OpenAI API key is missing. Please check your .env file.")

# Configure the OpenAI package globally for convenience
openai.api_key = api_key

def generate_script(prompt, model="gpt-3.5-turbo"):
    """Generate a short marketing video script using OpenAI models.

    The function first tries a chat-based completion. If the current API key
    does not have access to the specified chat model, it falls back to the
    ``text-davinci-003`` completion model.
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that writes marketing video "
                        "scripts."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except openai.PermissionDeniedError:
        # Fallback for API keys that cannot access chat models
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=(
                "You are a helpful assistant that writes marketing video scripts.\n"
                f"{prompt}"
            ),
            max_tokens=500,
        )
        return completion.choices[0].text.strip()

if __name__ == "__main__":
    input_prompt_path = "input/prompt.txt"
    output_script_path = "output/generated_script.txt"
    input_prompt_path = os.path.join(BASE_DIR, "input", "prompt.txt")
    output_script_path = os.path.join(BASE_DIR, "output", "generated_script.txt")

    if not os.path.exists(input_prompt_path):
        raise FileNotFoundError(f"Prompt file not found at {input_prompt_path}")

    with open(input_prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    script = generate_script(prompt)

    os.makedirs(os.path.dirname(output_script_path), exist_ok=True)
    with open(output_script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print("✅ Script generat cu succes:", output_script_path)
