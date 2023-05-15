from flask import Flask, request
import openai
from openai.error import RateLimitError
import sqlite3
from helpers import extract_code

# Set up the app
app = Flask(__name__)

# Set up an OpenAI API client with your API key
openai.api_key = "<your-api-key>"

# Get the database schema
rules_file = open('rules.txt', 'r')
rules = rules_file.read()

@app.route('/chat', methods=['POST'])
def get_sql():
    messages = [{"role": "user", "content": f"{rules}"}]
    request_data = request.json
    new_messages = request_data["messages"]
    for message in new_messages:
        if message["role"] == "user" or message["role"] == "assistant":
            messages.append(message)

    try:
        # Send the prompt to me for completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_content = response["choices"][0]["message"]["content"]

        code = extract_code(response_content)

        if code:
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            
            cur = con.cursor()
            cur.execute(code)
    
            rows = cur.fetchall()
            return {'reply': response_content, 'results': [tuple(row) for row in rows]}, 200

        return {'reply': response_content}


    except RateLimitError as RLE:
        return {'errors': RLE}, 400

if __name__ == '__main__':
    app.run()
