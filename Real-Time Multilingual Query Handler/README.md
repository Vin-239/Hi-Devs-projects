# Translation Web App

This is a simple web-based translation tool built with **Python** and **Flask**. It uses the **`translate`** library, which connects to the **MyMemory API** by default—a free and reliable service.

The app auto-detects the language of your input text and translates it directly to English, displaying the result instantly without reloading the page.

## Features
* **Simple Web Interface:** Runs in your browser.
* **Auto-Detect:** Automatically figures out the source language.
* **Stable API:** Uses the `MyMemory` translation service.
* **Instant Results:** The page doesn't reload; JavaScript fetches the translation in the background.
* **Lightweight:** No heavy AI models to download. Requires an internet connection.

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
    pip install Flask translate
    ```

## How to Run the App Locally

1.  Ensure all files are saved in the correct project structure as shown above.
2.  Open a terminal inside your main `Real-Time Multilingual Query Handler` folder.
3.  Make sure your virtual environment (`venv`) is activated.
4.  Run the Flask application:
    ```bash
    python app.py
    ```
5.  The terminal will show that the server is running, like this:
    `Server running at http://127.0.0.1:5000/`
6.  Open that `http://127.0.0.1:5000/` URL in your web browser to use the app. The server must remain running in your terminal.

## How It Works:

This project uses a client-server architecture:

1.  **Back-End (app.py):**
    * A **Flask** server runs on your machine.
    * It has one main page, which serves the `index.html` file from the `templates` folder.
    * It has a second "API" route (`/translate`). When it receives text, it uses the **`translate` library** (and its default MyMemory API) to automatically detect the source language and translate the text to English.
    * It then sends back *only* the translated text in a JSON format.

2.  **Front-End (HTML/CSS/JS):**
    * **`index.html`** provides the core structure of the webpage.
    * **`style.css`** (from the `static` folder) provides all the visual styling.
    * **`script.js`** (from the `static` folder) contains the application logic. It listens for the "Translate" button click, sends the text to the Flask back-end using `fetch()`, and updates the webpage with the result without a full page reload.
