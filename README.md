# **Movie Recommendation App API**

###### Project Members: Yan Chen, Jason Zhang


====

This project is about ...

# Requirements

## Usage


# Run the URL Shortener App Locally

1. Install virtual env on your local machine
    1. Windows User: python -m venv env
    2. Mac User: python3 -m venv env
2. Enable virtual env
    1. Windows User: source venv_pc
    2. Mac User: source venv_unix
3. Install dependencies
    1. Windows User: pip install -r requirements.txt
    2. Mac User: pip3 install -r requirements.txt
4. Run Flask App
    1. Windows User: python app.py
    2. Mac User: python3 app.py
5. OR run Flask App via Docker Container (docker installed)
    1. docker build -t flaskapp:latest .
    2. docker run -it -p 5000:5000 flaskapp
    3. Optional: docker run -it -d -p 5000:5000 flaskapp (automatically runs in background)
6.  Flask app runs on http://localhost:5000/

# Documentation