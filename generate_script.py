import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(dotenv_path="config/.env")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.strip() == "":
    raise ValueError("OpenAI API key is missing. Please check your .env file.")

client = OpenAI(api_key=api_key)

def generate_script(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes marketing video scripts."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    input_prompt_path = "input/prompt.txt"
    output_script_path = "output/generated_script.txt"

    if not os.path.exists(input_prompt_path):
        raise FileNotFoundError(f"Prompt file not found at {input_prompt_path}")

    with open(input_prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    script = generate_script(prompt)

    os.makedirs(os.path.dirname(output_script_path), exist_ok=True)
    with open(output_script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print("✅ Script generat cu succes:", output_script_path)
