import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_recommendations, preprocess_data, analyze_problem_courses

app = Flask(__name__)
CORS(app) 

@app.route('/recommend', methods=['POST'])
def recommend():
    student_data = request.json
    recommendations = get_recommendations(student_data)
    return jsonify(recommendations)

if __name__ == '__main__':
    data = preprocess_data(pd.read_csv('train.csv'))
    problem_courses, course_ruiners = analyze_problem_courses(data)
    app.run(debug=True)