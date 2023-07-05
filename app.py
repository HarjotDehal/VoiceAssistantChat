from flask import Flask, render_template, request, jsonify
import requests
import webbrowser
import openai
import os

from dotenv import find_dotenv, load_dotenv
app = Flask(__name__)

# OPENAI_API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"
# OPENAI_API_KEY = "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"

# API_KEY = open("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","r").read()

# API_KEY = "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"
# API_KEY =''

dotenv_path= find_dotenv()

load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")

openai.api_key=API_KEY


# openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    query = data["query"]
    response = handle_query(query)
    return response

def handle_query(query):
    words = query.lower().split()

    if "hello" in words:
        return "Hello! How can I assist you?"
    elif "goodbye" in words:
        return "Goodbye!"
    elif "open" in words:
        try:
            open_index = words.index("open")
            if open_index < len(words) - 1:
                url = "https://www." + words[open_index + 1] + ".com"
                webbrowser.open(url)
                return f"Opening {url}..."
            else:
                return "Please provide a URL to open after the 'open' keyword."
        except ValueError:
            return "I found 'open' in the query, but no URL was provided."
    else:
        answer = ask_question(query)
        return answer

chatlog =[]

def ask_question(question):
    # openai.api_key = OPENAI_API_KEY

    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=f"Question answering:\nContext: {question}\nQuestion: {question}",
    #     max_tokens=50
    # )
    chatlog.append({"role":"user","content":question})


    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=chatlog
    )
    assistantresponse = response['choices'][0]['message']['content']

    chatlog.append({"role":"assistant","content":assistantresponse.strip("\n").strip()})
    return("Your Input:" + question + "\n" "ChatGPT Response: \n" + assistantresponse.strip("\n").strip())

    # answer = response.choices[0].text.strip()
    # return answer

if __name__ == "__main__":
    app.run(debug=True)