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

MODEL = "llama3.2:3b"  # TODO: change to a model you pulled with `ollama pull`


def main() -> None:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "In one sentence, what is an inference engine?"},
        ],
    )
    print(response.choices[0].message.content)

    # TODO (reflection): in a comment or a print, explain in your own words
    # why this is "the same shape" as yesterday's hosted Gemini call.


if __name__ == "__main__":
    main()
