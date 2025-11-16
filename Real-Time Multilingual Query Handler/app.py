from flask import Flask, render_template, request, jsonify
# Import the new library
from translate import Translator

app = Flask(__name__)

translator = Translator(to_lang="en", from_lang="autodetect")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text_to_translate = data.get('text', '')

        print(f"Received text to translate: {text_to_translate}")

        if not text_to_translate:
            return jsonify({'translation': ''})

        translated_text = translator.translate(text_to_translate)
        
        print(f"Sending translation: {translated_text}")
        
        return jsonify({'translation': translated_text})
    
    except Exception as e:
        print(f"An error occurred: {e}") 
        error_message = f"Translation error: {e}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)