API-Based Translation Web App
This is a simple web-based translation tool built with Python and Flask. It uses the translate library, which connects to the MyMemory API by default—a free and reliable service.

The app auto-detects the language of your input text and translates it directly to English, displaying the result instantly without reloading the page.

Features
Simple Web Interface: Runs in your browser.

Auto-Detect: Automatically figures out the source language.

Stable API: Uses the MyMemory translation service.

Instant Results: The page doesn't reload; JavaScript fetches the translation in the background.

Lightweight: No heavy AI models to download. Requires an internet connection.

Project Structure
Your project folder must be organized as follows for Flask to find the files:

translator_project/
│
├── app.py              # The main Flask server & translation logic
│
├── templates/
│   └── index.html      # The HTML structure
│
└── static/
    ├── style.css       # The CSS for styling
    └── script.js       # The JavaScript for application logic
Installation
Create a virtual environment:

Bash

python -m venv venv
Activate the environment

Install the required libraries:

Bash

pip install Flask translate
How to Run the App Locally
Ensure all files are saved in the correct project structure as shown above.

Open a terminal inside your main translator project folder.

Make sure your virtual environment (venv) is activated.

Run the Flask application:

Bash

python app.py
The terminal will show that the server is running, like this: Server running at http://127.0.0.1:5000/

Open that http://127.0.0.1:5000/ URL in your web browser to use the app. The server must remain running in your terminal.

How It Works:
This project uses a client-server architecture:

Back-End (app.py):

A Flask server runs on your machine.

It has one main page (/) which serves the index.html file from the templates folder.

It has a second "API" route (/translate). When it receives text, it uses the translate library (and its default MyMemory API) to auto-detect the source and translate the text to English.

It then sends back only the translated text in a JSON format.

Front-End (HTML/CSS/JS):

index.html provides the core structure of the webpage.

style.css (from the static folder) provides all the visual styling.

script.js (from the static folder) contains the application logic. It listens for the "Translate" button click, sends the text to the Flask back-end using fetch(), and updates the webpage with the result without a full page reload.