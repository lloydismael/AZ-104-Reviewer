from flask import Flask, render_template, request, jsonify
import os
import json
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load questions data
def load_questions():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    try:
        with open(os.path.join(data_dir, 'az104_questions.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the JSON file doesn't exist yet, return an empty list
        return []

# Routes
@app.route('/')
def index():
    """Render the main quiz page"""
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    """Render the quiz interface page"""
    return render_template('quiz.html')

@app.route('/api/questions')
def get_questions():
    """API endpoint to get quiz questions"""
    questions = load_questions()
    
    # Check if we should limit number of questions
    limit = request.args.get('limit', default=None, type=int)
    if limit and limit < len(questions):
        questions = random.sample(questions, limit)
    
    return jsonify(questions)

@app.route('/api/question/<int:question_id>')
def get_question(question_id):
    """API endpoint to get a specific question by ID"""
    questions = load_questions()
    
    for question in questions:
        if question['id'] == question_id:
            return jsonify(question)
    
    return jsonify({"error": "Question not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
