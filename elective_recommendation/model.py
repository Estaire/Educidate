import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

data = pd.read_csv('train.csv')

def preprocess_data(data):
    data['Courses_Completed'] = data['Courses_Completed'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])

    def parse_course_attempts(attempts):
        if not isinstance(attempts, str):
            return {}
        items = attempts.split(' ')
        parsed = {}
        for i in range(0, len(items), 3):
            course_code = items[i]
            number_of_attempts = items[i+2] if (i+2) < len(items) else None
            parsed[course_code] = int(number_of_attempts) if number_of_attempts.isdigit() else None
        return parsed

    data['Course_Attempts'] = data['Course_Attempts'].apply(parse_course_attempts)

    def parse_course_difficulty(difficulty):
        if not isinstance(difficulty, str):
            return {}
        items = difficulty.split(' ')
        parsed = {}
        for i in range(0, len(items), 3):
            course_code = items[i]
            rating = items[i+2] if (i+2) < len(items) else None
            parsed[course_code] = int(rating) if rating.isdigit() else None
        return parsed

    data['Course_Difficulty'] = data['Course_Difficulty'].apply(parse_course_difficulty)
    return data

processed_data = preprocess_data(data)

def analyze_problem_courses(data):
    course_attempts = {}
    course_difficulty = {}
    course_ruiners = {}

    for _, row in data.iterrows():
        for course, attempts in row['Course_Attempts'].items():
            if attempts is not None:
                if course not in course_attempts:
                    course_attempts[course] = []
                course_attempts[course].append(attempts)

        for course, difficulty in row['Course_Difficulty'].items():
            if difficulty is not None:
                if course not in course_difficulty:
                    course_difficulty[course] = []
                course_difficulty[course].append(difficulty)

        for course in row['Courses_Completed']:
            if course not in course_ruiners:
                course_ruiners[course] = []
            course_ruiners[course].append(row['Course_Ruiners'])

    avg_attempts = {course: sum(attempts) / len(attempts) for course, attempts in course_attempts.items()}
    avg_difficulty = {course: sum(difficulty) / len(difficulty) for course, difficulty in course_difficulty.items()}

    problem_courses = []
    for course in avg_attempts:
        if avg_attempts[course] > 1 and avg_difficulty.get(course, 0) > 3:
            problem_courses.append(course)
    
    return problem_courses, course_ruiners

problem_courses, course_ruiners = analyze_problem_courses(processed_data)

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(processed_data['Course_Recommendations'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(student_data, cosine_sim=cosine_sim, problem_courses=problem_courses):
    completed_courses = student_data['Courses_Completed']

    course_indices = [i for i, course in enumerate(processed_data['Course_Recommendations']) if course not in completed_courses and course not in problem_courses]
    
    sim_scores = cosine_sim[course_indices].mean(axis=0)
    recommended_indices = sim_scores.argsort()[::-1]
    top_n_recommendations = [processed_data['Course_Recommendations'][i] for i in recommended_indices[:5]]
    return top_n_recommendations