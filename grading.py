import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import time
import os

ANTHONY = os.environ.get('ANTHONY').replace('\\n', '\n')


my_cred = {
  "type": "service_account",
  "project_id": "examai-0228",
  "private_key_id": "cb201016aa944bde90a2ab94f094a259cb63c2bd",
  "private_key": ANTHONY,
  "client_email": "firebase-adminsdk-cxdcl@examai-0228.iam.gserviceaccount.com",
  "client_id": "105408726183895905662",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-cxdcl%40examai-0228.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(my_cred)
firebase_admin.initialize_app(cred)
db = firestore.client()

def ask_gpt(question):
    key1 = "sk-XXofCUszTzeSX"
    key2 = "8HeAy85T3BlbkFJe"
    key3 = "lhWc2AUBFmbhRzFvwJD"
    keys = key1 + key2 + key3
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys}"
    }
    data = {
        # "model": "gpt-3.5-turbo",
        # "model": "gpt-4-turbo",
        # "model": "gpt-4",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a college professor who will grade assignments based on student submissions and rubrics. You will answer with a json and make sure the properly formatted and it has no syntax errors."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # This will raise an exception if the response contains an HTTP error status code
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content']
    return answer

# Function to load data from Firestore
def load_firebase(database):
    ref = db.collection(database)
    docs = ref.get()
    doc_names = [doc.id for doc in docs]  # Get document names (IDs)
    print("Document names in the collection:", doc_names)
    return [doc.to_dict() for doc in docs]

def grade_exam(exam_id):
    # Process each student's data
    exam_results = {
        "exam_id": exam_id,
        "students": []
    }

    professor_json = load_firebase("Professor")

    # Find the exam in all courses
    midterm_questions = None
    for course, course_data in professor_json[0].items():
        if "exams" in course_data and exam_id in course_data["exams"]:
            midterm_questions = course_data["exams"][exam_id]["questions"]
            break

    if midterm_questions is None:
        print(f"No exam found with id {exam_id}")
        return

    students_json = load_firebase("Student")

    # print(f"Grading exam {exam_id}")
    # print(f"content: {students_json}")

    for student_dict in students_json[0]["students"]:
        for student_id, answers in student_dict.items():
            # Print student['student_id'] and student_id
            # print(f"Processing student {student_id}")
            
            # Check if student is already graded
            doc_ref = db.collection('Graded').document(exam_id)
            doc = doc_ref.get()

            student_found = False

            if doc.exists:
                graded_students = doc.to_dict()["students"]
                for student in graded_students:
                    if student['student_id'] == student_id:
                        print(f"Skipping grading for student {student_id} as they are already graded.")
                        exam_results["students"].append(student)
                        student_found = True
                        break

            if student_found:
                continue

            student_result = {
                "student_id": student_id,
                "grades": [],
                "final_grade": 0
            }

            total_score = 0
            for question_dict in answers:
                for question_id, student_answer in question_dict.items():
                    question_number, student_question = next(((item['question_id'], item) for item in midterm_questions if item['text'] == question_id), (None, None))
                    if student_question and student_answer:
                        prompt = (
                            "Grade the answer from a student based on the given question and rubrics. "
                            "The question includes a set of rubrics, and weights asigned to each rubric. "
                            "The answer includes both the question and the student's response. "
                            "The output must be a json following this format using double quotes for keys: "
                            '{"question_id": <insert the Question here>, "rubric_scores": [<score1>, <score2>, ...], "total_score": <sum of all rubrics scores>, "feedback": "<Constructive feedback based on the students answer and how it could be improved>"}'
                            "Add your graded scores per rubric in the rubric_scores list based on your best assessment."
                            "DO NOT DEVIATE FROM THIS FORMAT, DOING SO WILL HURT MY PROGRAM. Print everything in one line.\n\n"
                            f"=============Question: {question_id}\n\n"
                            f"=============Rubrics: {student_question['rubrics']}\n\n"
                            f"=============Answer: {student_answer}\n\n"
                        )
                        graded_response = ask_gpt(prompt)
                        result_dict = json.loads(graded_response)
                        result_dict["answer"] = student_answer  # Add the student's answer
                        total_score += result_dict["total_score"]
                        result_dict["question_number"] = question_number
                        student_result["grades"].append(result_dict)
                        print(f"Graded question {question_number} for student {student_id}")
            student_result["final_grade"] = total_score
            exam_results["students"].append(student_result)

    # Output the final JSON
    exam_results_json = json.dumps(exam_results, indent=4)
    # print(exam_results_json)

    # Update the document in Firestore
    doc_ref = db.collection('Graded').document(exam_id)
    doc_ref.set(exam_results, merge=True)

exam_id = os.getenv('EXAM_ID')
student_id = os.getenv('STUDENT_ID')
print(f"Grading exam {exam_id}")
grade_exam(exam_id)
print("Grading completed.")