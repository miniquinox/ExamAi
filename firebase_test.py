import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import base64

# from dotenv import load_dotenv


# Load the environment variables from the .env file
# load_dotenv('FIREBASE_CREDENTIALS_JSON.env')

# # Get the JSON string from the environment variable
# my_cred = os.getenv('FIREBASE_CREDENTIALS_JSON')

# # Parse the JSON string into a Python dictionary
# my_cred_dict = json.loads(my_cred)

# # Use the dictionary to create the credentials
# cred = credentials.Certificate(my_cred_dict)

# # Initialize Firebase Admin with the credentials
# firebase_admin.initialize_app(cred)

# db = firestore.client()






# Fetch the base64 encoded JSON string from the environment variable
encoded_json = os.getenv('FIREBASE_CREDENTIALS_JSON_BASE64')
if not encoded_json:
    raise ValueError("Firebase credentials environment variable is not set.")

# Decode the base64 string
decoded_json = base64.b64decode(encoded_json).decode('utf-8')

# Convert the JSON string to a dictionary
firebase_credentials_dict = json.loads(decoded_json)

# Use the dictionary to initialize Firebase
cred = credentials.Certificate(firebase_credentials_dict)
firebase_admin.initialize_app(cred)


# Function to add or update student data in the exam
def add_student_to_exam(exam_id, student_data):
    # Reference to the specific exam in the 'Student' collection
    exam_ref = db.collection('Student').document(exam_id)

    # Check if the exam document exists
    exam = exam_ref.get()
    if exam.exists:
        # Update the exam document with the new student data
        exam_ref.update({
            f'students.{student_data["student_id"]}': student_data
        })
    else:
        # Create the exam document with the student data if it does not exist
        exam_ref.set({
            'students': {
                student_data['student_id']: student_data
            }
        })
    print(f'Added/Updated data for student {student_data["student_id"]} in exam {exam_id}.')

# Student data for stu005
student_data = {
    'student_id': 'stu001',
    'answers': [
        {"question_id": "Q1", "text": "Explanation for Q1 by stu005."},
        {"question_id": "Q2", "text": "Explanation for Q2 by stu005."},
        {"question_id": "Q3", "text": "Explanation for Q3 by stu005."}
    ]
}

# Add or update stu005 in Exam001
# add_student_to_exam('Exam001', student_data)


# Function to retrieve and save all data from the 'Student' collection
def save_and_print_all_students():
    students_ref = db.collection('Student')
    students = students_ref.get()

    all_students = [student.to_dict() for student in students]

    # Convert the data to a JSON string with indentation
    json_data = json.dumps(all_students, indent=4)

    # Print the JSON data
    print(json_data)

    # Save the JSON data to a file
    with open('student.json', 'w') as f:
        f.write(json_data)

# Call the function
save_and_print_all_students()