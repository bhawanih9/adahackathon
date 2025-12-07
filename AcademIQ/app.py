from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from agents.physics_tutor import PhysicsTutor
import os

app = Flask(__name__)
app.secret_key = 'super_secret_hackathon_key'

# Initialize Agent
# Ensure GOOGLE_API_KEY is set in environment
# Switched to gemini-2.0-flash-exp as requested
agent = PhysicsTutor(model_name='gemini-2.0-flash-exp') 

if os.environ.get("GOOGLE_API_KEY"):
     print("API Key found.")
else:
     print("WARNING: GOOGLE_API_KEY not found. Agent will fail.")

# Placeholder for current session data
mock_db = {}

# Fallback Data prevents app from breaking when API limit is hit
FALLBACK_DATA = {
    "topic": "Gravity (Demo Mode)",
    "kannada_explanation": "API ಮಿತಿ ಮೀರಿದೆ. ಇದು ಡೆಮೊ ವಿವರಣೆ: ಗುರುತ್ವಾಕರ್ಷಣೆಯು ವಸ್ತುಗಳನ್ನು ಕೆಳಕ್ಕೆ ಎಳೆಯುವ ಶಕ್ತಿಯಾಗಿದೆ.",
    "formula": "F = G * (m1 * m2) / r^2",
    "example": "When you drop an apple, it falls to the ground due to gravity.",
    "explanation": "API Rate Limit Hit. Showing Demo Content: Gravity is the force that pulls things towards the ground."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        user_question = request.form.get('question')
        user_age = request.form.get('age', 15) # Default to 15 if not provided
        session['age'] = user_age
        
        # Call Agent
        try:
            analysis = agent.analyze_question(user_question, user_age)
            session['topic_data'] = analysis
        except Exception as e:
            print(f"Agent Error: {e}")
            # Use useful fallback data instead of error message
            session['topic_data'] = FALLBACK_DATA
            
        return redirect(url_for('understanding'))
    return render_template('ask.html')

@app.route('/understanding')
def understanding():
    data = session.get('topic_data', {})
    if not isinstance(data, dict):
        # If somehow data is not a dict (e.g. string or list), force fallback or empty dict
        data = {} 
        
    topic = data.get('topic', 'Analyzing...')
    return render_template('understanding.html', topic=topic)

@app.route('/explanation')
def explanation():
    data = session.get('topic_data', {})
    return render_template('explanation.html', data=data)

@app.route('/diagram')
def diagram():
    data = session.get('topic_data', {})
    return render_template('diagram.html', data=data)

@app.route('/practice')
def practice():
    data = session.get('topic_data', {})
    topic = data.get('topic', 'General Physics')
    age = session.get('age', 15)
    
    try:
        quiz_data = agent.generate_quiz(topic, age)
        questions = quiz_data.get('questions', [])
        # Assign IDs just in case
        for idx, q in enumerate(questions):
            q['id'] = idx + 1
            
        session['current_quiz_questions'] = questions
        print(f"DEBUG: Generated Quiz List: {len(questions)} items")
    except Exception as e:
         print(f"Quiz Gen Error: {e}")
         questions = []

    return render_template('practice.html', questions=questions)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    answer = request.form.get('answer')
    q_id = int(request.form.get('q_id', 0))
    questions = session.get('current_quiz_questions', [])
    
    # Find question object
    quiz = next((q for q in questions if q['id'] == q_id), None)
    
    if not quiz:
        return jsonify({'correct': False, 'feedback': 'Error: Question not found.'})
    
    # Strip whitespace to be safe
    correct_answer = quiz.get('correct', '').strip()
    user_answer = answer.strip() if answer else ''
    
    correct = (user_answer.lower() == correct_answer.lower())
    feedback = quiz.get('feedback_correct') if correct else quiz.get('feedback_incorrect')
    return jsonify({'correct': correct, 'feedback': feedback})

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_msg = request.json.get('message')
    age = session.get('age', 15)
    
    response_text = agent.chat(user_msg, [], age)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
