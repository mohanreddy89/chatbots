from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'

# Initialize the dictionary to store user responses
user_responses = {}

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    
    # Store the user's response in the dictionary
    user_responses[len(user_responses) + 1] = message
    
    # Send the message to OpenAI's API and receive the response
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt="\n".join(user_responses.values()),
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    
    # Retrieve the system's response
    system_response = completion.choices[0].text.strip()
    
    # Provide guidance based on the user's question
    if "?" in message:
        system_response = "As an AI mental wellness assistant with 20 years of experience, I can provide guidance on various mental health topics. Feel free to ask any questions you have, and I'll do my best to assist you."
    elif "mental wellness" in message.lower() or "mental health" in message.lower():
        system_response = "Mental wellness is the state of well-being in which an individual realizes their own abilities, can cope with the normal stresses of life, can work productively, and is able to make a positive contribution to their community. It involves maintaining a balance in various aspects of life, including emotional, psychological, and social well-being."
    elif "stress management" in message.lower():
        system_response = "Stress management refers to techniques and strategies used to cope with or reduce stress. Some effective stress management techniques include deep breathing exercises, regular physical activity, practicing mindfulness or meditation, getting enough sleep, and engaging in activities you enjoy."
    else:
        system_response += "\n\nIf you have any other questions or need further assistance, feel free to ask."
    
    # Return the system's response
    return system_response

if __name__ == '_main_':
    app.run()