import ollama

def main():
    # Path to the visual asset in your lab directory
    image_path = "sample_chart.png" 
    prompt = "Analyze this chart. What are the key trends visible, and what does the data represent?"
    
    print("Sending multimodal request to local 'moondream' via native Ollama API...")
    
    try:
        response = ollama.chat(
            model="moondream",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_path]
                }
            ]
        )
        print("\n📊 Local VLM (moondream) Response:")
        print("-" * 50)
        print(response['message']['content'])
        print("-" * 50)
        
    except Exception as e:
        print(f"Error running moondream: {str(e)}")

if __name__ == "__main__":
    main()