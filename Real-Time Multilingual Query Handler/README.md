# Local LLM-Powered Translator Web App

This translator web app is a privacy-first translation tool powered by **Microsoft's Phi-3.5 Mini**, a state-of-the-art Small Language Model (SLM) running entirely locally via **Ollama**.

Unlike basic translation APIs, this application uses **Generative AI** and **Prompt Engineering** to contextually understand, detect, and translate text between 20+ languages with high accuracy, all without sending data to the cloud.

The app auto-detects the language of your input text and translates it directly to English, displaying the result instantly without reloading the page.

## Features
* **Edge AI Inference:** Powered by `phi3.5:latest` (3.8B parameters), running 100% offline on your CPU/GPU.
* **Prompt Engineering:** Uses a custom "System Prompt" pipeline to enforce strict translation rules and output formatting.
* **Multilingual Reasoning:** Leverages Phi-3.5's advanced training on synthetic and web data to handle complex linguistic nuances better than older models.
* **Simple Web Interface:** Runs in your browser.
* **Auto-Detect:** Automatically figures out the source language.
* **Instant Results:** The page doesn't reload; JavaScript fetches the translation in the background.
* **Zero Cost & Private:** No API keys, no monthly fees, and no data leakage.

## Project Structure
The project must be organized as follows for Flask to find the files:
```
Real-Time Multilingual Query Handler/ 
│ 
├── app.py # The main Flask server & translation logic
│ 
├── templates/ 
│   └── index.html # The HTML structure 
|
│── static/ 
    ├── style.css # The CSS for styling 
    └── script.js # The JavaScript for application logic
```

## Prerequisites

Before running the Python code, follow the steps given below (Important):

1.  **Install Ollama:** Download from [ollama.com](https://ollama.com).
2.  **Pull the Model:** Open your terminal and run the following command to download the specific model used in this project:
    ```bash
    ollama pull phi3.5
    ```
    * **Why this model?**  **Phi-3.5:latest** is a "high-quality, reasoning-dense" model optimized for multilingual tasks. At only ~2.2GB, it fits easily on consumer hardware while outperforming larger models in language understanding benchmarks.

## Installation

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
2.  **Activate the environment**:
    * Windows: `venv\Scripts\activate`
    * Mac/Linux: `source venv/bin/activate`

3.  **Install the required libraries**:
    ```bash
    pip install Flask ollama
    ```

## How to Run the App Locally

1.  Ensure all files are saved in the correct project structure as shown above.
2.  **Ensure Ollama is running** (You should see the llama icon in your system tray).
3.  Open a terminal inside your main `Real-Time Multilingual Query Handler` folder.
4.  Make sure your virtual environment (`venv`) is activated.
5.  Run the Flask application:
    ```bash
    python app.py
    ```
6.  The terminal will show that the server is running, like this:
    `Server running at http://127.0.0.1:5000/`
7.  Open that `http://127.0.0.1:5000/` URL in your web browser to use the app. The server must remain running in your terminal.

## How It Works:

1.  **Back-End (app.py):**
    * **Input:** User enters text (e.g., "Bonjour, comment ça va?") in the web UI.
    * **Prompt Construction:** The Flask backend wraps this input into a strict prompt structure:
    > *"You are a professional universal translator. Detect the source language and translate the user's text into clear, natural English. Output ONLY the English translation, without any quotes or explanations."*
    * **Local Inference:** The prompt is sent to the local Ollama instance hosting `phi3.5:latest`.
    * **Response:** The model uses its 128k context window and multilingual training to generate the English equivalent, which is returned to the user instantly.

2.  **Front-End (HTML/CSS/JS):**
    * **`index.html`** provides the core structure of the webpage.
    * **`style.css`** (from the `static` folder) provides all the visual styling.
    * **`script.js`** (from the `static` folder) contains the application logic. It listens for the "Translate" button click, sends the text to the Flask back-end using `fetch()`, and updates the webpage with the result without a full page reload.


