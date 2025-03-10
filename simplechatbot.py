from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__, template_folder='temp')

# Database Setup
def init_db():
    conn = sqlite3.connect("simple_chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chatbot_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route for Home Page
@app.route('/')
def home():
    return render_template('chat.html')

# Route for Chatbot Interaction
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    
    # Fetch response from database
    conn = sqlite3.connect("simple_chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM chatbot_responses WHERE question = ?", (user_input,))
    result = cursor.fetchone()
    
    if result:
        bot_response = result[0]
    else:
        bot_response = "Sorry, I don't understand that."
        cursor.execute("INSERT INTO chatbot_responses (question, response) VALUES (?, ?)", (user_input, bot_response))
        conn.commit()
    
    conn.close()
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
