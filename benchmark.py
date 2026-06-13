import requests

def run_benchmark(model_name, prompt):
    print(f"\n--- Testing {model_name} ---")
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False # Wait until the entire response is ready
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Ollama returns time in nanoseconds, convert to seconds (1 sec = 1,000,000,000 ns)
        load_time_sec = data.get("load_duration", 0) / 1e9
        eval_duration_sec = data.get("eval_duration", 0) / 1e9
        tokens = data.get("eval_count", 0)
        
        # Calculate tokens per second
        tps = tokens / eval_duration_sec if eval_duration_sec > 0 else 0
        
        print(f"Response: {data.get('response', '').strip()}\n")
        print(f"Load time (s): {load_time_sec:.2f}")
        print(f"Tokens/sec:    {tps:.2f}")
        print("-> NOW RECORD THE RAM USAGE IN 'ACTIVITY MONITOR' <-")
        
    except Exception as e:
        print(f"An error occurred. Is Ollama running in the background? Details: {e}")

# Fixed prompt for both models
fixed_prompt = "Explain the concept of local AI self-hosting in exactly two sentences."

# Run the tiny model first
run_benchmark("qwen2.5:0.5b", fixed_prompt)

input("\nPress Enter to proceed to the next model (record the RAM in your table now)...")

# Run the larger model
run_benchmark("phi3", fixed_prompt)