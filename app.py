import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

def draft_message(content, role='user'):
    return {
        "role": role,
        "content": content
    }

api_key = os.environ.get('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        messages = [
            {
                'role': 'system',
                'content': 'you are a professor with not so nice personality'
            },
            draft_message(user_input)
        ]
        
        chat_completion = client.chat.completions.create(
            temperature=1.0,
            n=1,
            model="mixtral-8x7b-32768",
            max_tokens=1000,
            messages=messages
        )
        
        bot_response = chat_completion.choices[0].message.content
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)