from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text_to_translate = data.get('text', '')

        print(f"User Input: {text_to_translate}")

        if not text_to_translate:
            return jsonify({'translation': ''})

        # --- PROMPT ENGINEERING START ---
        # We are using a Local LLM (Llama 3.2 via Ollama).
        # We construct a specific prompt to force it to act as a translator.
        
        system_prompt = "You are a professional universal translator. Detect the source language and translate the user's text into clear, natural English. Output ONLY the English translation, without any quotes or explanations."
        
        # Call the local Ollama model
        response = ollama.chat(model='phi3.5:latest', messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': text_to_translate,
            },
        ])

        # Extract the response content
        translated_text = response['message']['content'].strip()
        
        print(f"AI Response: {translated_text}")
        
        return jsonify({'translation': translated_text})
    
    except Exception as e:
        print(f"Error: {e}") 
        return jsonify({'error': f"Ollama Error: {str(e)}. Make sure Ollama is running!"}), 500

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)