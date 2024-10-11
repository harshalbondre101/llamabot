from flask import Flask, request, jsonify

app = Flask(__name__)

# Login to Hugging Face
from huggingface_hub import login
from llama_cpp import Llama

login('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')

# Initialize the model
llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Llama-3.2-1B-Instruct-GGUF",
    filename="Llama-3.2-1B-Instruct-Q3_K_L.gguf",
)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat with Llama Model</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            h1 {
                color: #333;
            }
            #chatbox {
                width: 400px;
                padding: 20px;
                border-radius: 10px;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            #user_input {
                width: 100%;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                margin-bottom: 10px;
            }
            #send_button {
                background-color: #5cb85c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
            #send_button:hover {
                background-color: #4cae4c;
            }
            #response {
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>Chat with Llama Model</h1>
        <div id="chatbox">
            <textarea id="user_input" rows="4" placeholder="Type your prompt here..."></textarea>
            <button id="send_button">Send</button>
            <div id="response"></div>
        </div>
        
        <script>
            document.getElementById('send_button').onclick = function() {
                const user_input = document.getElementById('user_input').value;
                fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'user_input=' + encodeURIComponent(user_input)
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').innerText = data.response;
                });
            };
        </script>
    </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    completion = llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return jsonify({'response': completion['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
