"""
Task 2 — Hit the local Ollama endpoint from Python.

Ollama exposes an OpenAI-compatible HTTP API on http://localhost:11434.
That means the SAME client code you used for a hosted API works here —
you only change the base URL (and the API key is a dummy value locally).

Run Ollama first (it starts a server automatically when you `ollama run`
or `ollama serve`), then:

    pip install -r requirements.txt
    python local_client.py
"""

from openai import OpenAI

# Point the OpenAI client at your LOCAL Ollama server instead of the cloud.
# This is the whole insight of the lab: "calling an LLM" is just an HTTP
# request to an inference server — wherever that server happens to run.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required by the client, but ignored by Ollama
)

# CHANGED: Updated to the model that successfully ran on your MacBook during Task 1.
MODEL = "qwen2.5:0.5b"  


def main() -> None:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "In one sentence, what is an inference engine?"},
        ],
    )
    print("🤖 Model Response:")
    print(response.choices[0].message.content)
    print("\n" + "="*50 + "\n")

    # REFLECTION: Explaining why this is "the same shape" as a hosted API call.
    print("🧠 REFLECTION: Why is this 'the same shape' as yesterday's hosted Gemini/OpenAI call?")
    print("Even though the AI is running entirely on my local MacBook, we are using the EXACT SAME")
    print("OpenAI Python SDK. The code structure, the 'chat.completions.create' method, and the")
    print("JSON message format (system/user roles) are 100% identical.")
    print("The ONLY things changed are:")
    print("  1. The 'base_url' -> pointing to 'localhost:11434' instead of a remote cloud server.")
    print("  2. The 'model' name -> pointing to our local 'qwen2.5:0.5b'.")
    print("  3. The 'api_key' -> just a dummy string.")
    print("This proves that an LLM is simply an inference engine behind an API endpoint. Whether")
    print("it lives in a massive cloud data center or locally on my machine, the HTTP communication")
    print("protocol remains exactly the same.")


if __name__ == "__main__":
    main()